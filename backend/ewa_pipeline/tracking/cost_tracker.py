"""Accumulate token usage and calculate per-phase model cost."""

import json
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


OPENAI_FALLBACK_PRICING: dict[str, dict[str, float]] = {
    # Official OpenAI standard API pricing per 1M text tokens, checked 2026-07-22.
    # Azure pricing may differ; config.yaml can override by model or deployment name.
    "gpt-5.6-sol": {
        "input_per_1m": 5.00,
        "cached_input_per_1m": 0.50,
        "cache_write_per_1m": 6.25,
        "output_per_1m": 30.00,
    },
    "gpt-5.6-terra": {
        "input_per_1m": 2.50,
        "cached_input_per_1m": 0.25,
        "cache_write_per_1m": 3.125,
        "output_per_1m": 15.00,
    },
    "gpt-5.6-luna": {
        "input_per_1m": 1.00,
        "cached_input_per_1m": 0.10,
        "cache_write_per_1m": 1.25,
        "output_per_1m": 6.00,
    },
    # The unqualified alias routes to Sol.
    "gpt-5.6": {
        "input_per_1m": 5.00,
        "cached_input_per_1m": 0.50,
        "cache_write_per_1m": 6.25,
        "output_per_1m": 30.00,
    },
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
    cache_write_tokens: int = 0
    output_tokens: int = 0


class CostTracker:
    """Accumulate token usage across all pipeline phases and calculate cost."""

    def __init__(self, pricing: dict[str, dict[str, float]]):
        self.pricing = pricing
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
        cache_write_tokens: int = 0,
    ) -> None:
        with self._lock:
            if phase not in self._entries:
                self._entries[phase] = _Entry(phase=phase, model=model)
            entry = self._entries[phase]
            entry.calls += 1
            entry.input_tokens += input_tokens
            cached = min(cached_input_tokens, input_tokens)
            entry.cached_input_tokens += cached
            entry.cache_write_tokens += min(
                cache_write_tokens,
                max(input_tokens - cached, 0),
            )
            entry.output_tokens += output_tokens

    @staticmethod
    def _canonical_model(model: str) -> str:
        value = model.lower()
        for known_model in sorted(OPENAI_FALLBACK_PRICING, key=len, reverse=True):
            if known_model in value:
                return known_model
        return value

    def _pricing_for(self, model: str) -> dict[str, float]:
        canonical = self._canonical_model(model)
        return (
            self.pricing.get(model)
            or self.pricing.get(canonical)
            or OPENAI_FALLBACK_PRICING.get(canonical, {})
        )

    def _cost(
        self,
        model: str,
        input_tokens: int,
        cached_input_tokens: int,
        cache_write_tokens: int,
        output_tokens: int,
    ) -> tuple[float, float, float, float]:
        pricing = self._pricing_for(model)
        billable_input_tokens = max(
            input_tokens - cached_input_tokens - cache_write_tokens,
            0,
        )
        input_cost = billable_input_tokens / 1_000_000 * pricing.get("input_per_1m", 0.0)
        cached_input_cost = (
            cached_input_tokens / 1_000_000 * pricing.get("cached_input_per_1m", 0.0)
        )
        cache_write_cost = (
            cache_write_tokens / 1_000_000 * pricing.get("cache_write_per_1m", 0.0)
        )
        output_cost = output_tokens / 1_000_000 * pricing.get("output_per_1m", 0.0)
        return input_cost, cached_input_cost, cache_write_cost, output_cost

    def to_dict(self, document_name: str = "") -> dict:
        breakdown = []
        notes = [
            "Prices come from config.yaml when present; otherwise known OpenAI standard API rates are used as a fallback.",
            "Azure model pricing may differ from OpenAI standard API pricing.",
            "Document normalization token usage is not included here.",
        ]
        total_calls = total_input = total_cached_input = total_cache_write = total_output = 0
        total_cost = 0.0

        for entry in self._entries.values():
            pricing = self._pricing_for(entry.model)
            billable_input_tokens = max(
                entry.input_tokens - entry.cached_input_tokens - entry.cache_write_tokens,
                0,
            )
            input_cost, cached_input_cost, cache_write_cost, output_cost = self._cost(
                entry.model,
                entry.input_tokens,
                entry.cached_input_tokens,
                entry.cache_write_tokens,
                entry.output_tokens,
            )
            entry_cost = input_cost + cached_input_cost + cache_write_cost + output_cost

            breakdown.append(
                {
                    "phase": entry.phase,
                    "model": entry.model,
                    "calls": entry.calls,
                    "input_tokens": entry.input_tokens,
                    "cached_input_tokens": entry.cached_input_tokens,
                    "cache_write_tokens": entry.cache_write_tokens,
                    "billable_input_tokens": billable_input_tokens,
                    "output_tokens": entry.output_tokens,
                    "pricing": {
                        "input_per_1m": pricing.get("input_per_1m", 0.0),
                        "cached_input_per_1m": pricing.get("cached_input_per_1m"),
                        "cache_write_per_1m": pricing.get("cache_write_per_1m"),
                        "output_per_1m": pricing.get("output_per_1m", 0.0),
                    },
                    "input_cost_usd": round(input_cost, 6),
                    "cached_input_cost_usd": round(cached_input_cost, 6),
                    "cache_write_cost_usd": round(cache_write_cost, 6),
                    "output_cost_usd": round(output_cost, 6),
                    "total_cost_usd": round(entry_cost, 6),
                }
            )

            total_calls += entry.calls
            total_input += entry.input_tokens
            total_cached_input += entry.cached_input_tokens
            total_cache_write += entry.cache_write_tokens
            total_output += entry.output_tokens
            total_cost += entry_cost

            if not pricing:
                notes.append(
                    f"No pricing configured for model '{entry.model}'; its run cost is reported as 0."
                )
            elif entry.cached_input_tokens > 0 and pricing.get("cached_input_per_1m") is None:
                notes.append(
                    f"Model '{entry.model}' used cached input tokens, but cached_input_per_1m is not configured; cached token cost is reported as 0."
                )
            elif entry.cache_write_tokens > 0 and pricing.get("cache_write_per_1m") is None:
                notes.append(
                    f"Model '{entry.model}' used cache-write tokens, but cache_write_per_1m is not configured; cache-write token cost is reported as 0."
                )

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "document": document_name,
            "breakdown": breakdown,
            "totals": {
                "calls": total_calls,
                "input_tokens": total_input,
                "cached_input_tokens": total_cached_input,
                "cache_write_tokens": total_cache_write,
                "billable_input_tokens": max(
                    total_input - total_cached_input - total_cache_write,
                    0,
                ),
                "output_tokens": total_output,
                "total_tokens": total_input + total_output,
                "cost_usd": round(total_cost, 6),
            },
            "notes": list(dict.fromkeys(notes)),
        }

    def save(self, path: Path, document_name: str = "") -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(document_name), indent=2), encoding="utf-8")
