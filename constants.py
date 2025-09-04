from importlib.metadata import version, PackageNotFoundError
import pathlib
import tomllib
from scrts import PROXIES, MONGO_URI

# config
PRINT_REQUESTS: bool = True
MONGO_DATABASE: str = "2bwikiscrape"
WIKI_BASE_URL: str = "https://2b2t.miraheze.org/wiki/"
WIKI_API_URL: str = "https://2b2t.miraheze.org/w/api.php"

# pyproject shit
with open('pyproject.toml', 'rb') as file:
    PYPROJECT_DATA: dict = tomllib.load(file)
VERSION: str = PYPROJECT_DATA["project"]["version"]
GITHUB_URL: str = PYPROJECT_DATA["project"]["urls"]["Repository"]
USER_AGENT: str = f"2bWikiScrape/{VERSION} ({GITHUB_URL})"


# load secrets
PROXIES: set[str] = PROXIES
MONGO_URI: str = MONGO_URI
