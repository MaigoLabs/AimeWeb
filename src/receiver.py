import re
import time
from pathlib import Path

import uvicorn
import winsound
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from vk import press_key, release_key

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
PATH = Path('aime.txt')
AUDIO_EFFECT = Path(__file__).parent / 'audio/mixkit-gaming-lock-2848.wav'


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
    press_key()
    time.sleep(5)
    release_key()

    return {"uid": uid}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8249)
