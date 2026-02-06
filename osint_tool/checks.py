import dataclasses
import time
from typing import Iterable, Optional

import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import requests

DEFAULT_PLATFORMS = {
    "github": "https://github.com/{username}",
    "twitter": "https://twitter.com/{username}",
    "instagram": "https://www.instagram.com/{username}/",
    "linkedin": "https://www.linkedin.com/in/{username}/",
    "reddit": "https://www.reddit.com/user/{username}/",
    "tiktok": "https://www.tiktok.com/@{username}",
    "medium": "https://medium.com/@{username}",
    "pinterest": "https://www.pinterest.com/{username}/",
    "youtube": "https://www.youtube.com/@{username}",
}


@dataclasses.dataclass
class PhoneResult:
    raw: str
    e164: Optional[str]
    valid: bool
    possible: bool
    region: Optional[str]
    description: Optional[str]
    carrier: Optional[str]
    timezones: list[str]


@dataclasses.dataclass
class SocialResult:
    platform: str
    url: str
    exists: Optional[bool]
    status_code: Optional[int]


def lookup_phone(number: str, region: str = "US") -> PhoneResult:
    parsed = phonenumbers.parse(number, region)
    valid = phonenumbers.is_valid_number(parsed)
    possible = phonenumbers.is_possible_number(parsed)
    description = geocoder.description_for_number(parsed, "en") or None
    carrier_name = carrier.name_for_number(parsed, "en") or None
    timezones = list(timezone.time_zones_for_number(parsed))
    region_code = phonenumbers.region_code_for_number(parsed) or None
    e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    return PhoneResult(
        raw=number,
        e164=e164,
        valid=valid,
        possible=possible,
        region=region_code,
        description=description,
        carrier=carrier_name,
        timezones=timezones,
    )


def check_social_username(
    username: str,
    platforms: Optional[dict[str, str]] = None,
    timeout: float = 8.0,
    delay_s: float = 0.5,
) -> list[SocialResult]:
    targets = platforms or DEFAULT_PLATFORMS
    results: list[SocialResult] = []
    session = requests.Session()
    for platform, template in targets.items():
        url = template.format(username=username)
        exists = None
        status_code = None
        try:
            response = session.get(url, timeout=timeout, allow_redirects=True)
            status_code = response.status_code
            if status_code == 200:
                exists = True
            elif status_code in {301, 302, 403, 404}:
                exists = status_code != 404
            else:
                exists = None
        except requests.RequestException:
            exists = None
        results.append(
            SocialResult(
                platform=platform,
                url=url,
                exists=exists,
                status_code=status_code,
            )
        )
        time.sleep(delay_s)
    return results


def summarize_social(results: Iterable[SocialResult]) -> dict[str, list[SocialResult]]:
    buckets: dict[str, list[SocialResult]] = {"found": [], "not_found": [], "unknown": []}
    for result in results:
        if result.exists is True:
            buckets["found"].append(result)
        elif result.exists is False:
            buckets["not_found"].append(result)
        else:
            buckets["unknown"].append(result)
    return buckets
