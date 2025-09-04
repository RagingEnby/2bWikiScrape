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
        for page in pages:
            if page.ns != 0:
                print(page.to_dict())
                
        #page = random.choice(pages.pages)
        #await asyncio.gather(
        #    do_page(page),
        #    do_page(pages.query('popbob'))
        #)
        await do_page(pages.query('popbob'))
    finally:
        await close()


if __name__ == "__main__":
    asyncio.run(main())