import asyncio


async def nested():
    return 42


async def main():
    task = asyncio.create_task(nested())
    await task


if __name__ == '__main__':
    print(asyncio.run(main()))
