import math, yaml
# TODO: Add better calibration code support
class morse():
    def __init__(self):
        self.morsechart = {'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.', 'g': '--.',
                           'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.',
                           'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.', 's': '...', 't': '-', 'u': '..-',
                           'v': '...-', 'w': '.--', 'x': '-..-', 'y': '-.--', 'z': '--..'}

        stream = open('settings.yaml', 'r')
        self.settings = yaml.load(stream)
        stream.close()
        self.offset = 0.09
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
            if len(words) > 0:
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

        for x in dits:
            avgDit += arr[x]
        avgDit /= 3

        for x in dahs:
            avgDah += arr[x]
        avgDah /= 3


        for x in pauses:
            avgPause += arr[x]
        avgPause /= 5
        avgPause /= 2
        avgPause = round(avgPause, 2)


        self.settings['space'] = arr[0]
        for x in arr:
            if x > self.settings['space']:
                self.settings['space'] = x

        self.settings['ditRange'] = [round(avgDit-self.offset, 2), round(avgDit+self.offset, 2)]
        self.settings['dahRange'] = [round(avgDah - 0.07, 2)]
        self.settings['pauseRange'] = [avgPause, self.settings['space']]
    def get_pause_range(self):
        return self.settings['pauseRange']
    def get_space(self):
        return self.settings['space']
    def is_calibrated(self):
        return self.settings['calibrated']
    def save_calibration(self):
        self.settings['calibrated'] = "y"
        stream = open('settings.yaml', 'w')
        yaml.dump(self.settings, stream)
        stream.close()

    def print_calib_results(self):
        print("dit: " + str(self.settings['ditRange']))
        print("dah: " + str(self.settings['dahRange'] ))
        print("pause: " + str(self.settings['pauseRange']))
        print("space: " + str(self.settings['space']))


    def to_morse_string(self, arr):
        morseString = ""
        for x in arr:
            if self.settings['ditRange'][0] <= x <= self.settings['ditRange'][1]:
                morseString += "."
            elif x >= self.settings['dahRange'][0]:
                morseString += "-"
            else:
                if x < self.settings['ditRange'][0] :
                    morseString += '.'
                elif x > self.settings['ditRange'][1]:
                    morseString += "-"

        return morseString


