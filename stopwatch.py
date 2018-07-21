import time
class stopwatch():
    def __init__(self):
        self.running = False
        self.timer = time;
    def start(self):
        if not self.running:
            self.running = True
            self.startTime = self.timer.time()
        else:
            raise Warning("Stopwatch is already running!")

    def stop(self):
        if self.running:
            self.running = False
            self.endTime = self.timer.time()
        else:
            raise Warning("Stopwatch not running!")
    def is_running(self):
        return self.running
    def get_elapsed(self):
        if not self.running:
            return self.endTime - self.startTime
        else:
            return self.timer.time() - self.startTime