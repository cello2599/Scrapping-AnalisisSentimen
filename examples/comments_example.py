import asyncio
import json

from pytok.tiktok import PyTok

videos = [
    {
        'id': '7266454099518819589',
        'author': {
            'uniqueId': 'celooa'
        }
    }
]

async def main():
    async with PyTok(headless=False) as api:
        for video in videos:
            comments = []
            async for comment in api.video(id=video['id'], username=video['author']['uniqueId']).comments(count=1000):
                comments.append(comment)

            with open("komentar2.json", "w") as f:
                json.dump(comments, f)

if __name__ == "__main__":
    asyncio.run(main())
