# asyncgTTS

Asynchronous interfaces to the [official Google Text to Speech](https://cloud.google.com/text-to-speech) or [easygTTS](https://github.com/Gnome-py/easy-gtts-api) APIs written with aiohttp.  

## Examples

### asyncgTTS
```python
import asyncio
import asyncgTTS
from subprocess import PIPE, run

async def main():
    token = run(['gcloud', 'auth', 'application-default', 'print-access-token'], stdout=PIPE).stdout.decode().replace("\n", "")
    async with await asyncgTTS.setup(premium=True, auth_token=token) as gtts:
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
import asyncgTTS
import asyncio

async def main():
    async with await asyncgTTS.setup(premium=False) as gtts:
        hello_world = await gtts.get(text="Hello World")
    
    with open("Hello_world.mp3", "wb") as f:
        f.write(hello_world)

asyncio.run(main())
```