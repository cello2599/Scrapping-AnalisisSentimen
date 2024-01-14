import asyncio
import json

from pytok.tiktok import PyTok

async def main():
    async with PyTok() as api:
        user = api.user(username="celooa")
        user_data = await user.info()
        with open("coba_scrap.json", "w") as f:
            json.dump(user_data, f)

        videos = []
        async for video in user.videos():
            if len(video) > 2:
                break
            video_data = video.info()
            videos.append(video_data)

        assert len(videos) > 0, "No videos found"
        with open("out.json", "w") as f:
            json.dump(videos, f)

if __name__ == "__main__":
    asyncio.run(main())
