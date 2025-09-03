import curl_cffi
from urllib.parse import urlencode

import constants


SESSION: curl_cffi.AsyncSession | None = None
PROXY_INDEX: int = 0


async def get_session() -> curl_cffi.AsyncSession:
    global SESSION
    if SESSION is None:
        SESSION = curl_cffi.AsyncSession(
            timeout=15,
            impersonate="chrome110"
        )
    return SESSION


def choose_proxy() -> str:
    global PROXY_INDEX
    proxies = list(constants.PROXIES)
    index = PROXY_INDEX % len(proxies)
    PROXY_INDEX = index + 1
    return proxies[index]


async def close():
    global SESSION
    if SESSION is not None:
        await SESSION.close()
        SESSION = None


async def get(*args, **kwargs) -> curl_cffi.Response:
    session = await get_session()
    response = await session.get(*args, **kwargs)
    if constants.PRINT_REQUESTS:
        full_url = f"{args[0]}?{urlencode(kwargs['params'])}" if kwargs.get('params') else args[0]
        print('GET' + (' PROXY' if kwargs.get('proxy') else ''), response.status_code, full_url)
    return response
    
    
async def proxy_get(*args, **kwargs) -> curl_cffi.Response:
    impersonate = kwargs.pop('impersonate', 'chrome110')
    return await get(
        *args,
        proxy=choose_proxy(),
        impersonate=impersonate,
        **kwargs
        )
    
    
async def post(*args, **kwargs) -> curl_cffi.Response:
    session = await get_session()
    response = await session.post(*args, **kwargs)
    return response


async def proxy_post(*args, **kwargs) -> curl_cffi.Response:
    impersonate = kwargs.pop('impersonate', 'chrome110')
    return await post(
        *args,
        proxy=choose_proxy(),
        impersonate=impersonate,
        **kwargs
    )
    