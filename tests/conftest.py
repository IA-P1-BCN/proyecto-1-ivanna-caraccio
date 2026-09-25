import os
import sys


CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(CURRENT_DIR, "..", "src")

sys.path.insert(0, os.path.abspath(SRC_DIR))
