import os

SRC_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_PATH = os.path.dirname(SRC_PATH)
DATA_PATH = os.path.join(PROJECT_PATH, "data")
COGS_PATH = os.path.join(SRC_PATH, "cogs")
TEMP_PATH = os.path.join(DATA_PATH, "temp")
