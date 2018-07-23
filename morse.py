import math
class morse():
    def __init__(self):
        self.morsechart = {'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..', 'g': '--.',
                           'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.',
                           'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.', 's': '...', 't': '-', 'u': '..-',
                           'v': '...-', 'w': '.--', 'x': '-..-', 'y': '-.--', 'z': '--..'}
        self.ditRange = []
        self.dahRange = []
        self.pause = 0.00
        self.space = 0

        self.offset = 0.02
    def to_morse(self, string=""):
        morseString = ""
        for c in string.lower():
            if c.isalpha():
                morseString += self.morsechart.get(c) + " "
            elif c.isspace():
                morseString += "  "
        return morseString

    def to_alpha(self, string=""):
        retString = ""
        words = string.split("  ")
        for w in words:
            word = ""
            letters = w.split()
            for c in letters:
                for alpha, morse in self.morsechart.items():
                    if c == morse:
                        word += str(alpha)
            retString += word + " "

        #print(arr)
        return retString
    def calibrate(self, arr):
        dits = [0, 2, 4]
        dahs = [8, 10, 12]
        pauses = [1, 3, 5, 9, 11]
        avgPause = 0
        avgDit = 0
        avgDah = 0
        avgSpace = 0
        for x in dits:
            avgDit += arr[x]
        avgDit /= 3
        avgDit = round(avgDit, 2)
        for x in dahs:
            avgDah += arr[x]
        avgDah /= 3
        avgDah = round(avgDah, 2)

        for x in pauses:
            self.pause += arr[x]
        self.pause /= 5
        self.pause /= 2
        self.pause = round(self.pause, 2)

        self.space = arr[0]
        for x in arr:
            if x > self.space:
                self.space = x

        self.ditRange = [round(avgDit-self.offset, 2), round(avgDit+self.offset, 2)]
        self.dahRange = [round(avgDah - self.offset, 2), round(avgDah + self.offset, 2)]




    def print_calib_results(self):
        print("dit: " + str(self.ditRange))
        print("dah: " + str(self.dahRange))
        print("pause: " + str(self.pause))
        print("space: " + str(self.space))

    def get_space(self):
        return self.space
    def get_pause(self):
        return self.pause

    def to_morse_string(self, arr):
        morseString = ""
        for x in arr:
            if self.ditRange[0] <= x <= self.ditRange[1]:
                morseString += "."
            elif self.dahRange[0] <= x <= self.dahRange[1]:
                morseString += "-"
            else:
                print(x)
                raise ValueError("Input doesn't match calibration values!")
        return morseString


