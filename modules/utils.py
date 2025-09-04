import aiofiles


async def write(file_name: str, content: str):
    async with aiofiles.open(file_name, 'w', encoding='utf-8') as file:
        await file.write(content)
        