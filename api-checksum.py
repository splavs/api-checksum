import aiohttp
import asyncio


def checksum(element):
    element_type = type(element)
    if element_type is int:
        return element
    elif element_type is str:
        return sum(ord(e) for e in element)


def calculate_checksum(data):
    res = 0
    for d in data:
        # res += (124567890 + checksum(d)) * checksum(d)
        res += checksum(d)
    return res


async def get_single_api_checksum(session, url):
    async with session.get(url) as resp:
        api_resp = await resp.text()
        return [url, calculate_checksum(api_resp)]


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, 15):
            url = f'https://pokeapi.co/api/v2/pokemon/{i}'
            tasks.append(asyncio.ensure_future(get_single_api_checksum(session, url)))

        result = await asyncio.gather(*tasks)
        final_checksum = 0
        for r in result:
            print(r)
            final_checksum += r[1]

        print("Final checksum: ", final_checksum)


asyncio.run(main())
