"""Profile configurations for different transit providers."""

import os
import ssl
import urllib3
from dataclasses import dataclass
from typing import Optional
from pyhafas.profile import DBProfile, NVVProfile, VSNProfile

# Disable SSL warnings when SSL verification is disabled
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@dataclass
class TransitProfile:
    """Configuration for a transit provider."""

    name: str
    country: str
    description: str
    hafas_profile: any
    language: str = "en"
    timezone: str = "Europe/Berlin"


# Available transit profiles
PROFILES = {
    "oebb": TransitProfile(
        name="ÖBB",
        country="Austria",
        description="Austrian Federal Railways (Österreichische Bundesbahnen)",
        hafas_profile=DBProfile(),  # Using DB profile as fallback for ÖBB
        language="de",
        timezone="Europe/Vienna"
    ),
    "db": TransitProfile(
        name="Deutsche Bahn",
        country="Germany",
        description="German Federal Railway (Deutsche Bahn)",
        hafas_profile=DBProfile(),
        language="de",
        timezone="Europe/Berlin"
    ),
    "sbb": TransitProfile(
        name="SBB",
        country="Switzerland",
        description="Swiss Federal Railways (Schweizerische Bundesbahnen)",
        hafas_profile=DBProfile(),  # Using DB profile as fallback for SBB
        language="de",
        timezone="Europe/Zurich"
    ),
    "ns": TransitProfile(
        name="NS",
        country="Netherlands",
        description="Nederlandse Spoorwegen (Dutch Railways)",
        hafas_profile=DBProfile(),  # Using DB profile as fallback for NS
        language="en",
        timezone="Europe/Amsterdam"
    ),
    "nvv": TransitProfile(
        name="NVV",
        country="Germany",
        description="Nordhessischer Verkehrsverbund",
        hafas_profile=NVVProfile(),
        language="de",
        timezone="Europe/Berlin"
    ),
    "vsn": TransitProfile(
        name="VSN",
        country="Germany",
        description="Verkehrsverbund Süd-Niedersachsen",
        hafas_profile=VSNProfile(),
        language="de",
        timezone="Europe/Berlin"
    ),
}


def get_profile(profile_name: str) -> Optional[TransitProfile]:
    """Get a transit profile by name.

    Args:
        profile_name: Name of the profile (e.g., 'oebb', 'db', 'sbb', 'ns')

    Returns:
        TransitProfile if found, None otherwise
    """
    return PROFILES.get(profile_name.lower())


def list_profiles() -> list[dict]:
    """List all available transit profiles.

    Returns:
        List of profile information dictionaries
    """
    return [
        {
            "id": key,
            "name": profile.name,
            "country": profile.country,
            "description": profile.description,
            "language": profile.language,
        }
        for key, profile in PROFILES.items()
    ]
