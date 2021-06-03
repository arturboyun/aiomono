import asyncio

from aiomonobank import MonoClient


async def main():
    cli = MonoClient()
    async with cli as client:
        print(await client.get_currency())


if __name__ == '__main__':
    asyncio.run(main())
