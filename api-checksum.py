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
        with open('urls.txt', 'r') as file:
            urls = file.read().splitlines()
            for url in urls:
                tasks.append(asyncio.ensure_future(get_single_api_checksum(session, url)))

        result = await asyncio.gather(*tasks)
        total_checksum = 0
        for r in result:
            print(r[0], r[1])
            total_checksum += r[1]

        print("Total checksum: ", total_checksum)


asyncio.run(main())
