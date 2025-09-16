import requests


def geocode_postcode(postcode: str):
    """
    Use postcodes.io to resolve a UK postcode into latitude/longitude.
    Support all UK nations including Scotland postcodes.
    """
    if not postcode:
        return None, None

    clean = postcode.replace(" ", "").upper()
    url = f"https://api.postcodes.io/postcodes/{clean}"
    try:
        r = requests.get(
            url,
            headers={"Accept": "application/json"},
            timeout=5,
        )
        data = r.json()
        if r.status_code == 200 and data.get("status") == 200:
            return (
                data["result"]["latitude"],
                data["result"]["longitude"],
            )
    except Exception:
        pass
    return None, None
