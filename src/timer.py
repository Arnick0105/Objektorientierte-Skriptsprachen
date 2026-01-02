import time
from settings import *

class GameTimer:
    def __init__(self):
        self.start_time = time.time()

    def remaining(self):
        elapsed = time.time() - self.start_time
        return max(0, TIME_LIMIT - int(elapsed))
