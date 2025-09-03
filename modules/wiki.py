from urllib.parse import urlencode
from modules import asyncreqs

URL: str = "https://2b2t.miraheze.org/w/api.php?action=parse&page=Main%20Page&format=json"


async def get_page(page: str) -> str:
    params = {
        "action": "parse",
        "page": page,
        "format": "json"
    }
    