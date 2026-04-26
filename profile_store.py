import json
import os

PROFILE_PATH = "memory/profiles.json"


def save_profile(name: str, profile: dict):
    """Save a user profile to disk."""
    os.makedirs("memory", exist_ok=True)
    profiles = load_all_profiles()
    profiles[name] = profile
    with open(PROFILE_PATH, "w") as f:
        json.dump(profiles, f, indent=2)


def load_profile(name: str) -> dict | None:
    """Load a single user profile by name."""
    profiles = load_all_profiles()
    return profiles.get(name)


def load_all_profiles() -> dict:
    """Load all saved profiles."""
    if not os.path.exists(PROFILE_PATH):
        return {}
    with open(PROFILE_PATH, "r") as f:
        return json.load(f)


def delete_profile(name: str):
    """Delete a profile."""
    profiles = load_all_profiles()
    if name in profiles:
        del profiles[name]
        with open(PROFILE_PATH, "w") as f:
            json.dump(profiles, f, indent=2)
