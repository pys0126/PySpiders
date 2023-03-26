import asyncio
import aiohttp

url = "https://ref.moneyguru.co/uodrad123"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64"
}
tasks = []


def main():
    for i in range(400):
        task = asyncio.ensure_future(send())
        tasks.append(task)


async def send():
    async with aiohttp.ClientSession() as Session:
        async with Session.get(url=url, headers=headers) as response:
            print(response.status)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    main()
    loop.run_until_complete(asyncio.wait(tasks))
