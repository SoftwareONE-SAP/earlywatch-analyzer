"""
CostTracker - accumulates token usage per phase and model, calculates cost,
and saves a _cost.json report alongside the other output artifacts.
"""

import json
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

OPENAI_FALLBACK_PRICING: dict[str, dict[str, float]] = {
    # Official OpenAI standard API pricing per 1M text tokens, checked 2026-06-07.
    # Azure deployments may be named after these models; config.yaml can override.
    "gpt-5.4": {
        "input_per_1m": 2.50,
        "cached_input_per_1m": 0.25,
        "output_per_1m": 15.00,
    },
    "gpt-5.4-mini": {
        "input_per_1m": 0.75,
        "cached_input_per_1m": 0.075,
        "output_per_1m": 4.50,
    },
    "gpt-5.4-nano": {
        "input_per_1m": 0.20,
        "cached_input_per_1m": 0.02,
        "output_per_1m": 1.25,
    },
}


@dataclass
class _Entry:
    phase: str
    model: str
    calls: int = 0
    input_tokens: int = 0
    cached_input_tokens: int = 0
    output_tokens: int = 0


class CostTracker:
    """Accumulate token usage across all pipeline phases and calculate cost."""

    def __init__(self, pricing: dict[str, dict[str, float]]):
        """
        pricing: {
            deployment_name: {
                "input_per_1m": float,
                "cached_input_per_1m": float,
                "output_per_1m": float,
            }
        }
        """
        self.pricing = {**OPENAI_FALLBACK_PRICING, **pricing}
        self._entries: dict[str, _Entry] = {}
        self._lock = threading.Lock()

    def record(
        self,
        phase: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        *,
        cached_input_tokens: int = 0,
    ) -> None:
        with self._lock:
            if phase not in self._entries:
                self._entries[phase] = _Entry(phase=phase, model=model)
            entry = self._entries[phase]
            entry.calls += 1
            entry.input_tokens += input_tokens
            entry.cached_input_tokens += min(cached_input_tokens, input_tokens)
            entry.output_tokens += output_tokens

    def _cost(
        self,
        model: str,
        input_tokens: int,
        cached_input_tokens: int,
        output_tokens: int,
    ) -> tuple[float, float, float]:
        pricing = self.pricing.get(model, {})
        billable_input_tokens = max(input_tokens - cached_input_tokens, 0)
        input_cost = billable_input_tokens / 1_000_000 * pricing.get("input_per_1m", 0.0)
        cached_input_cost = (
            cached_input_tokens / 1_000_000 * pricing.get("cached_input_per_1m", 0.0)
        )
        output_cost = output_tokens / 1_000_000 * pricing.get("output_per_1m", 0.0)
        return input_cost, cached_input_cost, output_cost

    def to_dict(self, document_name: str = "") -> dict:
        breakdown = []
        notes = [
            "Prices come from config.yaml when present; otherwise known OpenAI model rates are used as a fallback.",
            "Document normalization token usage is not included here.",
        ]
        total_calls = total_input = total_cached_input = total_output = 0
        total_cost = 0.0

        for entry in self._entries.values():
            pricing = self.pricing.get(entry.model, {})
            billable_input_tokens = max(entry.input_tokens - entry.cached_input_tokens, 0)
            input_cost, cached_input_cost, output_cost = self._cost(
                entry.model,
                entry.input_tokens,
                entry.cached_input_tokens,
                entry.output_tokens,
            )
            entry_cost = input_cost + cached_input_cost + output_cost

            breakdown.append(
                {
                    "phase": entry.phase,
                    "model": entry.model,
                    "calls": entry.calls,
                    "input_tokens": entry.input_tokens,
                    "cached_input_tokens": entry.cached_input_tokens,
                    "billable_input_tokens": billable_input_tokens,
                    "output_tokens": entry.output_tokens,
                    "pricing": {
                        "input_per_1m": pricing.get("input_per_1m", 0.0),
                        "cached_input_per_1m": pricing.get("cached_input_per_1m"),
                        "output_per_1m": pricing.get("output_per_1m", 0.0),
                    },
                    "input_cost_usd": round(input_cost, 6),
                    "cached_input_cost_usd": round(cached_input_cost, 6),
                    "output_cost_usd": round(output_cost, 6),
                    "total_cost_usd": round(entry_cost, 6),
                }
            )

            total_calls += entry.calls
            total_input += entry.input_tokens
            total_cached_input += entry.cached_input_tokens
            total_output += entry.output_tokens
            total_cost += entry_cost

            if entry.model not in self.pricing:
                notes.append(
                    f"No pricing configured for model '{entry.model}'; its run cost is reported as 0."
                )
            elif entry.cached_input_tokens > 0 and pricing.get("cached_input_per_1m") is None:
                notes.append(
                    f"Model '{entry.model}' used cached input tokens, but cached_input_per_1m is not configured; cached token cost is reported as 0."
                )

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "document": document_name,
            "breakdown": breakdown,
            "totals": {
                "calls": total_calls,
                "input_tokens": total_input,
                "cached_input_tokens": total_cached_input,
                "billable_input_tokens": max(total_input - total_cached_input, 0),
                "output_tokens": total_output,
                "total_tokens": total_input + total_output,
                "cost_usd": round(total_cost, 6),
            },
            "notes": list(dict.fromkeys(notes)),
        }

    def save(self, path: Path, document_name: str = "") -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(document_name), indent=2), encoding="utf-8")
