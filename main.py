"""Entry point: spins up vision + reasoner threads and waits."""

import threading
import time

from vision_agent import VisionAgent
from reasoner_agent import ReasonerAgent
from shared_state import SharedState


def main():
    state = SharedState()
    vision = VisionAgent(state)
    reasoner = ReasonerAgent(state)

    vision.start()
    reasoner.start()

    print("PlayerTwo is running. Press Ctrl+C to stop.")
    # Wait forever, but keep main thread alive so Ctrl‑C works nicely
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down PlayerTwo...")


if __name__ == "__main__":
    main()
