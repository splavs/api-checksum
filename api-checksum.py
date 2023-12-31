import aiohttp
import asyncio
import time

start_time = time.time()


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


async def get_api_checksum(session, url):
    async with session.get(url) as resp:
        api_resp = await resp.text()
        return calculate_checksum(api_resp)


async def get_apis_checksum(session, urls, param_value):
    tasks = []
    for url in urls:
        tasks.append(asyncio.ensure_future(get_api_checksum(session, url)))
    checksums = await asyncio.gather(*tasks)
    return [param_value, sum(checksums)]


async def process_urls(params_values, urls_values):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=100)) as session:
        tasks = []
        for param_value in params_values:
            urls = [url_value.format(param_value) for url_value in urls_values]
            tasks.append(asyncio.ensure_future(get_apis_checksum(session, urls, param_value)))

        return await asyncio.gather(*tasks)


async def print_checksums(result):
    total_checksum = 0
    print("checksum calculated for all apis for each param")
    for r in result:
        print(f"param: {r[0]}, checksum: {r[1]}")
        total_checksum += r[1]
    print(f"checksum for all apis for all params: {total_checksum}")


async def read_data(file_name):
    with open(file_name, 'r') as file:
        data = file.read().splitlines()
    return data


async def main(urls_file_name, parameter_values_file_name):
    urls_values = await read_data(urls_file_name)
    params_values = await read_data(parameter_values_file_name)

    result = await process_urls(params_values, urls_values)
    await print_checksums(result)


if __name__ == '__main__':
    asyncio.run(main('urls.txt', 'parameter_values.txt'))

    runtime = time.time() - start_time
    print(f"done in {runtime}s")
