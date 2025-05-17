"""Thread that periodically turns raw log into story narration."""

from __future__ import annotations

import threading
import time
import ollama
from typing import List, Dict, Any


import config
from shared_state import SharedState

client = ollama.Client()


class ReasonerAgent(threading.Thread):
    def __init__(self, state: SharedState):
        super().__init__(daemon=True)
        self.state = state

    def run(self):
        while True:
            self.state.wait_for_new_raw_logs()  # Wait for enough new raw logs

            story_ctx = self.state.recent_story(config.STORY_CONTEXT_WINDOW)
            # Use RAW_LOGS_PER_SUMMARY for the raw context window to match the trigger condition
            raw_ctx = self.state.recent_raw(config.RAW_LOGS_PER_SUMMARY) 

            if raw_ctx:  # Should always be true now due to wait_for_new_raw_logs
                new_story = reason_over_raw(
                    config.REASONER_MODEL,
                    story_ctx=story_ctx,
                    raw_ctx=raw_ctx,
                )
                if "Error:" not in new_story:
                    self.state.append_story(new_story)
                else:
                    print(f"ReasonerAgent: Story not appended due to error in generation: {new_story}")
                print(f"\n[STORY] {new_story}\n")
            
            self.state.reset_new_raw_logs_count() # Reset counter after summarization


def reason_over_raw(model: str, story_ctx: str, raw_ctx: str) -> str:
    """Ask the reasoning LLM to extend the narrative story."""

    prompt = (
        "You are summarizing a stream of observations of a user's computer "
        "activity, based on snapshot descriptions of screenshots of their computer "
        "every few seconds. Given the new raw observations below, extend the last summary by 1-3 sentences. " "There may be discontinuities "
        "between observations, that's ok, don't try too hard to connect unrelated events, just let them be "
        "separate. Be aware that there could be many duplicative raw observations, that is normal, as the user's screen could be static for a while as they read or watch something. That is why you're here, to take the raw observations and summarize into a condensed log of potentially hours of time.\n" 
        "If nothing new has happened since the last summary, your summary can be very short.\n\n" +
        f"Past summaries:\n{story_ctx}\n\n" +
        f"New raw observations from the last minute or so:\n{raw_ctx}\n\n" +
        "Return ONLY the new summary continuation."
    )

    messages: List[Dict[str, Any]] = [
        {"role": "user", "content": prompt}
    ]

    response = client.chat(model=model, messages=messages)
    return response["message"]["content"].strip()
