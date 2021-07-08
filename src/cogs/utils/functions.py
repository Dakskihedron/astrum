import aiohttp


def date(target):
    return target.strftime('%a, %d %b %Y @ %I:%M:%S %p')


async def get_data(url):
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as r:
            data = await r.json()
            try:
                r.raise_for_status()
                return data, None
            except aiohttp.ClientResponseError as e:
                status = e.status
                return data, status
            except aiohttp.web.Exception as e:
                print(e)