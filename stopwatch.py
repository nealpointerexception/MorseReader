import time
class stopwatch():
    def __init__(self):
        self.time = time
        self.running = False

    def start(self):
        if not self.running:
            self.running = True
        else:
            raise Warning("Stopwatch is already running!")
        self.startTime = time.time()
    def end(self):
        if self.running:
            self.running = False
            self.endTime = time.time()
        else:
            raise Warning("Stopwatch not running!")
    def is_running(self):
        return self.running
    def get_elapsed(self):
        if not self.running:
            return self.endTime - self.startTime
        else:
            return self.time.time() - self.startTime