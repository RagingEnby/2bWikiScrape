import asyncio
import json

from modules import asyncreqs
from modules import wiki
import constants


async def main():
    try:
        tasks = [asyncreqs.proxy_get(wiki.URL) for _ in range(len(constants.PROXIES))]
        responses = await asyncio.gather(*tasks)
        codes = set(response.status_code for response in responses)
        if codes != {200}:
            print('Some proxies failed')
            for response in responses:
                if response.status_code != 200:
                    print(response.text)
        print("Response codes:", codes)
    finally:
        await asyncreqs.close()


if __name__ == "__main__":
    asyncio.run(main())