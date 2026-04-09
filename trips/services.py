import requests


class ArtInstituteService:
    BASE_URL = "https://api.artic.edu/api/v1/artworks"

    @classmethod
    def get_artwork(cls, external_id: int):
        try:
            response = requests.get(f"{cls.BASE_URL}/{external_id}", timeout=10)
        except requests.RequestException:
            return None

        if response.status_code != 200:
            return None

        data = response.json().get("data")
        if not data:
            return None

        return {
            "id": data["id"],
            "title": data.get("title"),
        }
