import asyncio

from pytok.tiktok import PyTok

username = 'celooa'
id = '7244707606256684293'

async def main():
    async with PyTok() as api:
        video = api.video(username=username, id=id)

        # Bytes of the TikTok video
        video_data = await video.info()
        # video_bytes = await video.bytes()

        with open("out.json", "w") as out_file:
            out_file.write(video_data)

if __name__ == "__main__":
    asyncio.run(main())
