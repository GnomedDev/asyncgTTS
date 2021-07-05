# asyncgTTS

Asynchronous interfaces to the [official Google Text to Speech](https://cloud.google.com/text-to-speech) or [easygTTS](https://github.com/Gnome-py/easy-gtts-api) APIs written with aiohttp.  

## Examples

### asyncgTTS
```python
import asyncio
from subprocess import PIPE, run

import aiohttp
import asyncgTTS

async def main():
    async with aiohttp.ClientSession() as session:
        gtts = await asyncgTTS.setup(premium=True, session=session, service_account_json_location="SERVICE_ACCOUNT.json")

        hello_world_ogg = await gtts.get("Hello World", voice_lang=("en-US-Standard-B", "en-us"))
        hello_world_mp3 = await gtts.get("Hello World", voice_lang=("en-US-Standard-A", "en-us"), ret_type="MP3")

    with open("Hello_world.ogg", "wb") as f:
        f.write(hello_world_ogg)
    with open("Hello_world.mp3", "wb") as f:
        f.write(hello_world_mp3)

asyncio.run(main())
```

### easygTTS
```python
import asyncio

import aiohttp
import asyncgTTS

async def main():
    async with aiohttp.ClientSession() as session:
        gtts = await asyncgTTS.setup(premium=False, session=session)
        hello_world = await gtts.get(text="Hello World")

    with open("Hello_world.mp3", "wb") as f:
        f.write(hello_world)

asyncio.run(main())
```