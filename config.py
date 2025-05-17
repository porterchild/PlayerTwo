VISION_MODEL = "gemma3:4b-it-qat"   
REASONER_MODEL = "gemma3:4b-it-qat" ## "qwen3:4b" would be good, but same model reduces memory usage...          

SCREENSHOT_INTERVAL = 5              # seconds between screenshots
RAW_LOGS_PER_SUMMARY = 5             # number of raw logs before a story update

RAW_CONTEXT_WINDOW = 5              # most‑recent raw lines sent as context
STORY_CONTEXT_WINDOW = 100            # most‑recent story lines sent as context
