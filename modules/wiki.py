import re
import asyncio
from typing import Self
from html import unescape
from urllib.parse import quote

from modules import asyncreqs
import constants


request_semaphore: asyncio.Semaphore = asyncio.Semaphore(10)


class Page:
    def __init__(self, title: str, page_id: int, ns: int | None = None):
        self.title = title
        self.page_id = page_id
        self.ns = ns or 0
        self._content = None
        
    @property
    def markdown(self) -> str:
        if not self._content:
            raise ValueError("Content not loaded")
        return mediawiki_to_markdown(self._content)
        
    async def get_content(self) -> str:
        if self._content is None:
            page_data = await get_page_data(self.title)
            self._content = page_data.content
        return self._content
    
    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "pageid": self.page_id,
            "ns": self.ns
        }
        
    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(data['title'], data['pageid'], data.get('ns'))
    
    
class PageData(Page):
    def __init__(self, title: str, page_id: int, content: str, ns: int | None = None):
        super().__init__(title, page_id, ns or 0)
        self.content = content
        
    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "pageid": self.page_id,
            "ns": self.ns,
            "content": self.content
        }
        
    @classmethod
    async def from_page(cls, page: Page) -> Self:
        content = await page.get_content()
        return cls(
            title=page.title,
            page_id=page.page_id,
            content=content,
            ns=page.ns
        )
    
    
class Pages:
    def __init__(self, pages: list[Page]):
        self.pages = pages
        self.index = 0
        
    def query(self, query: str) -> Page:
        partial_match: Page | None = None
        fuzzy_match: Page | None = None
        for page in self.pages:
            if query.lower() == page.title.lower():
                return page
            elif page.title.lower().startswith(query.lower()):
                partial_match = page
            elif query.lower() in page.title.lower():
                fuzzy_match = page
        match = partial_match or fuzzy_match
        if not match:
            raise ValueError(f"No page found for query: {query}")
        return match
        
    async def __aiter__(self):
        self.index = 0
        return self
    
    async def __anext__(self):
        if self.index >= len(self.pages):
            raise StopAsyncIteration
        page = self.pages[self.index]
        self.index += 1
        return await page.get_content()
    
    def __iter__(self):
        return self.pages.__iter__()
    
    def extend(self, pages: list[Page] | Self):
        if isinstance(pages, Pages):
            self.pages.extend(pages.pages)
        else:
            self.pages.extend(pages)
    
    def to_dict(self) -> list[dict]:
        return [page.to_dict() for page in self.pages]
    
    @classmethod
    def from_dict(cls, data: list[dict]) -> Self:
        return cls([Page.from_dict(page) for page in data])


async def get_all_pages() -> Pages:
    apcontinue = None
    pages = Pages([])
    while True:
        params = {
            "action": "query",
            "list": "allpages",
            "aplimit": "max",
            "format": "json",
            "formatversion": 2
        }
        if apcontinue:
            params["apcontinue"] = apcontinue

        response = await asyncreqs.proxy_get(constants.WIKI_API_URL, params=params)
        data = response.json()
        pages.extend(Pages.from_dict(data['query']['allpages']))

        if 'continue' in data and 'apcontinue' in data['continue']:
            apcontinue = data['continue']['apcontinue']
        else:
            break
    return pages
    

async def get_page_data(page_name: str) -> PageData:
    async with request_semaphore:
        params = {
            "action": "query",
            "prop": "revisions",
            "titles": page_name,
            "rvprop": "content",
            "format": "json",
            "formatversion": 2
        }
        response = await asyncreqs.proxy_get(constants.WIKI_API_URL, params=params)
        data = response.json()
        page_info = data['query']['pages'][0]
        revision_content = page_info['revisions'][0]['content']
        return PageData(
            title=page_info['title'],
            page_id=page_info['pageid'],
            content=revision_content
        )
        
        
async def test(page_name: str) -> str:
    async with request_semaphore:
        params = {
            "action": "query",
            "prop": "extracts",
            "titles": page_name,
            "explaintext": True,
            "exsectionformat": "plain",
            "format": "json",
            "formatversion": 2
        }
        response = await asyncreqs.proxy_get(constants.WIKI_API_URL, params=params)
        data = response.json()
        raw_extract = data['query']['pages'][0]['extract']
        cleaned_extract = re.sub(r'\[edit \| edit source\]', '', raw_extract).strip()
        return cleaned_extract
    
    
def mediawiki_to_markdown(wikitext: str) -> str:
    text = wikitext.replace("\r\n", "\n").replace("\r", "\n")

    title = None
    m = re.search(r"\{\{\s*DISPLAYTITLE\s*:\s*([^}]+)\}\}", text, flags=re.I)
    if m:
        title = m.group(1).strip()
    else:
        m = re.search(
            r"\{\{\s*PlayerTemplate\b.*?\|\s*title\s*=\s*([^\n|}]+)",
            text,
            flags=re.I | re.S,
        )
        if m:
            title = m.group(1).strip()

    text = re.sub(
        r"\{\{\s*DISPLAYTITLE\s*:[^}]+\}\}", "", text, flags=re.I
    )
    text = re.sub(r"\{\{\s*Pp-pc[^}]*\}\}", "", text, flags=re.I)
    text = re.sub(
        r"\{\{\s*PlayerTemplate\b.*?\}\}", "", text, flags=re.I | re.S
    )

    text = re.sub(r"<ref[^/>]*/>", "", text, flags=re.I)
    text = re.sub(
        r"<ref[^>]*>.*?</ref>", "", text, flags=re.I | re.S
    )
    text = re.sub(r"<references[^>]*/>", "", text, flags=re.I)

    text = re.sub(
        r"\[\[(?:File|Image):.*?\]\]", "", text, flags=re.I | re.S
    )
    text = re.sub(r"\[\[\s*Category:[^\]]+\]\]", "", text, flags=re.I)

    text = re.sub(r"'''''(.*?)'''''", r"***\1***", text, flags=re.S)
    text = re.sub(r"'''(.*?)'''", r"**\1**", text, flags=re.S)
    text = re.sub(r"''(.*?)''", r"*\1*", text, flags=re.S)

    def _heading(mh: re.Match) -> str:
        level = len(mh.group(1))
        content = mh.group(2).strip()
        return f"{'#' * level} {content}"

    text = re.sub(
        r"^(={1,6})\s*(.*?)\s*\1\s*$", _heading, text, flags=re.M
    )

    def _wikilink(mw: re.Match) -> str:
        inner = mw.group(1).strip()
        if inner.startswith(("Category:", "File:", "Image:")):
            return ""
        parts = inner.split("|", 1)
        target = parts[0].strip()
        label = parts[1].strip() if len(parts) > 1 else target

        if target.startswith(":"):
            target = target[1:]

        if "#" in target:
            page, anchor = target.split("#", 1)
        else:
            page, anchor = target, None

        page_path = quote(page.replace(" ", "_"), safe="()!~*._-:")
        if anchor:
            anchor_id = quote(anchor.replace(" ", "_"), safe="()!~*._-:")
            url = f"{constants.WIKI_BASE_URL}{page_path}#{anchor_id}"
        else:
            url = f"{constants.WIKI_BASE_URL}{page_path}"

        return f"[{label}]({url})"

    text = re.sub(r"\[\[([^[\]]+)\]\]", _wikilink, text)

    def _ext(mex: re.Match) -> str:
        url = mex.group(1)
        label = mex.group(2).strip() if mex.group(2) else url
        return f"[{label}]({url})"

    text = re.sub(
        r"\[(https?://[^\s\]]+)(?:\s+([^\]]+))?\]", _ext, text
    )

    text = unescape(text)
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    if title:
        if text:
            return f"# {title}\n\n{text}"
        return f"# {title}"
    return text
