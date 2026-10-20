"""Deploy an existing single-container app and migrate legacy model settings atomically."""
from __future__ import annotations

import argparse
import json
import subprocess


MODEL_ALIASES = {
    "ORCHESTRATOR_MODEL": "V2_ORCHESTRATOR_MODEL",
    "SPECIALIST_MODEL": "V2_SPECIALIST_MODEL",
    "CHAT_MODEL": "V2_ORCHESTRATOR_MODEL",
}
MODEL_NAMES = sorted(set(MODEL_ALIASES) | set(MODEL_ALIASES.values()))
MODEL_FILTER = " || ".join(f"name=='{name}'" for name in MODEL_NAMES)
SETTINGS_QUERY = (
    "{container:properties.template.containers[0].name,"
    f"models:properties.template.containers[0].env[?{MODEL_FILTER}]."
    "{name:name,value:value,secretRef:secretRef},"
    "legacyNames:properties.template.containers[0].env[?starts_with(name,'V2_')].name}"
)


def migration(settings: dict) -> tuple[list[str], list[str]]:
    """Only seed missing current names; preserve every explicit Portal selection."""
    models = {item["name"]: item for item in settings.get("models") or []}

    def value(name):
        item = models.get(name, {})
        if item.get("secretRef"):
            return "secretref:" + item["secretRef"]
        return (item.get("value") or "").strip()

    additions = []
    for current, legacy in MODEL_ALIASES.items():
        if value(current):
            continue
        inherited = value(legacy)
        if not inherited:
            raise ValueError(f"Configure {current} on the Container App before deployment.")
        additions.append(f"{current}={inherited}")
    removals = sorted({name for name in settings.get("legacyNames") or [] if name.startswith("V2_")})
    return additions, removals


def deploy(app: str, resource_group: str, image: str) -> None:
    common = ["--name", app, "--resource-group", resource_group, "--only-show-errors"]
    # Read values only for known model settings. Credentials and other settings
    # are neither fetched nor replaced; Azure merges the narrowly scoped update.
    result = subprocess.run(["az", "containerapp", "show", *common, "--query", SETTINGS_QUERY,
                             "--output", "json"], check=True, capture_output=True, text=True)
    settings = json.loads(result.stdout)
    additions, removals = migration(settings)
    command = ["az", "containerapp", "update", *common, "--container-name", settings["container"],
               "--image", image]
    if additions:
        command += ["--set-env-vars", *additions]
    if removals:
        command += ["--remove-env-vars", *removals]
    command += ["--query", "{image:properties.template.containers[0].image,revision:properties.latestRevisionName}",
                "--output", "json"]
    subprocess.run(command, check=True)
    print(f"Model settings migration: {len(additions)} missing names populated; {len(removals)} legacy names removed.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", required=True)
    parser.add_argument("--resource-group", required=True)
    parser.add_argument("--image", required=True)
    args = parser.parse_args()
    try:
        deploy(args.app, args.resource_group, args.image)
    except ValueError as exc:
        parser.exit(1, f"{exc}\n")
    except subprocess.CalledProcessError as exc:
        parser.exit(1, f"Azure CLI deployment command failed with exit code {exc.returncode}.\n")


if __name__ == "__main__":
    main()
