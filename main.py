import asyncio
import random
import json
import constants

from modules import asyncreqs
from modules import wiki
from modules import utils


async def close():
    try:
        await asyncreqs.close()
    except Exception as e:
        print('unable to close asyncreqs session:', e)
        
        
async def do_page(page: wiki.Page):
    content = await page.get_content()
    await asyncio.gather(
        utils.write(f'output/pages/{page.title}.txt', content),
        utils.write(f'output/pages/{page.title}.md', page.markdown)
    )
        

async def main():
    try:
        pages = await wiki.get_all_pages()
        await utils.write(f'output/all_pages.json', json.dumps(pages.to_dict(), indent=2))
                
        chunk_size = 50
        chunks = [pages.pages[i:i + chunk_size] for i in range(0, len(pages.pages), chunk_size)]
        results = await asyncio.gather(*[
            wiki.bulk_get_page_data(set(page.title for page in chunk))
            for chunk in chunks
        ])
        page_datas = [page_data for result in results for page_data in result]
        print('!! got', len(page_datas), 'in', len(results), 'requests')
        await asyncio.gather(*[
            utils.write(f'output/pages/{page.safe_title}.md', page.markdown)
            for page in page_datas
        ])
    finally:
        await close()


if __name__ == "__main__":
    asyncio.run(main())