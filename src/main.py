import re
import time
from pathlib import Path

import uvicorn
import winsound
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse

from vk import press_key, release_key


AIME_PATH = "aime.txt"      # segatools aimePath
KEY = 0x0D                  # segatools card scan key
PORT = 8249                 # HTTP Port


app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
PATH = Path(AIME_PATH)
AUDIO_EFFECT = Path(__file__).parent / 'audio/mixkit-gaming-lock-2848.wav'

HTML = Path(__file__).parent.parent / "web/dist/index.html"


@app.get("/", response_class=HTMLResponse)
def read_root():
    return HTML.read_text()


@app.post("/scan")
def scan(uid: str):
    """
    Parse the UID from the raw input string.
    """
    uid = uid.replace(":", "")

    # If the UID is 16-digit hex, treat it as a Felica and convert that to a 20-digit int
    if re.match(r'^[0-9a-fA-F]{16}$', uid):
        uid = str(int(uid, 16))

    # Else if uid is a 20-digit int, use it
    elif re.match(r'^\d{20}$', uid):
        pass

    # Else, raise an error
    else:
        raise HTTPException(status_code=400, detail="Invalid UID format")

    PATH.write_text(uid)

    # Play sound
    winsound.PlaySound(str(AUDIO_EFFECT), winsound.SND_FILENAME)

    # Simulate key press
    press_key(KEY)
    time.sleep(5)
    release_key(KEY)

    return {"uid": uid}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8249)
