import aiofiles
import asyncio


file_semaphore: asyncio.Semaphore = asyncio.Semaphore(10)


async def write(file_name: str, content: str):
    async with file_semaphore, aiofiles.open(file_name, 'w', encoding='utf-8') as file:
        await file.write(content)
        