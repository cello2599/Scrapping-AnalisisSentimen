import asyncio
import json

from pytok.tiktok import PyTok

async def main():
    async with PyTok(headless=True) as api:
        user = api.user(username="celooa")
        # get random user to load page
        user_data = await user.info()
        with open("coba_scrap.json", "w") as f:
            json.dump(user_data, f)
        ms_tokens = await api.get_ms_tokens()
        print(ms_tokens)

if __name__ == "__main__":
    asyncio.run(main())
