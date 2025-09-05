# lat/lang for rough geolocation
import requests

def geocode_uk_postcode(postcode: str):
    cleaned = postcode.strip().upper().replace('-', '').replace('.', '')
    r = requests.get(f"https://api.postcodes.io/postcodes/{cleaned}", timeout=10)
    data = r.json()
    if r.status_code == 200 and data.get("status") == 200:
        res = data["result"]
        return {
            "postcode": res["postcode"],  # normalized UK postcode eg. N22 8AA
            "lat": res["latitude"],
            "lng": res["longitude"],
        }
    return None
