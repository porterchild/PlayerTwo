"""Thread that captures the screen & appends raw log lines."""

from __future__ import annotations

import threading
import time

import mss
from PIL import Image
import ollama
import base64
from io import BytesIO
from typing import List, Dict, Any


import config
from shared_state import SharedState

client = ollama.Client()


class VisionAgent(threading.Thread):
    def __init__(self, state: SharedState):
        super().__init__(daemon=True)
        self.state = state
        self.sct = None # Initialize sct to None

    def _grab_screen(self) -> Image.Image:
        if self.sct is None: # Initialize mss here if not already initialized
            self.sct = mss.mss()
        mon = self.sct.monitors[0]  # full screen
        raw = self.sct.grab(mon)
        return Image.frombytes("RGB", raw.size, raw.rgb)

    def run(self):
        screenshot_count = 0
        while True:
            img = self._grab_screen()
            
            screenshot_count += 1

            description = vision_describe(
                model=config.VISION_MODEL,
                img=img
            )

            self.state.append_raw(description)
            print(f"[RAW] {description}")
            time.sleep(config.SCREENSHOT_INTERVAL)


def _encode_image(img: Image.Image) -> str:
    """Return base64‑encoded PNG string for Ollama vision messages."""
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


def vision_describe(model: str, img: Image.Image) -> str:
    """Send screenshot to a vision model and return its reply."""
    img_b64 = _encode_image(img)

    messages: List[Dict[str, Any]] = [
        {
            "role": "user",
            "content": "Describe this user screenshot with as much detail as you can in 2 or 3 sentences. Respond only with your description.",
            "images": [img_b64],
        }
    ]

    try:
        response = client.chat(model=model, messages=messages)
        if response and "message" in response and "content" in response["message"]:
            return response["message"]["content"].strip()
        else:
            print(f"vision_describe: Error - Unexpected response format from Ollama: {response}")
            return "Error: Could not get description from vision model."
    except Exception as e:
        print(f"vision_describe: Exception during Ollama API call: {e}")
        return f"Error: Exception during vision model call - {e}"
