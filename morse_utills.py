import math, yaml
# TODO: Add better calibration code support


class Morse:
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
        morse_string = ""
        for c in string.lower():
            if c.isalpha():
                morse_string += self.morsechart.get(c) + " "
            elif c.isspace():
                morse_string += "  "
        return morse_string

    def to_alpha(self, string=""):
        ret_string = ""
        words = string.split("  ")
        for w in words:
            word = ""
            letters = w.split()
            for c in letters:
                for alpha, morse in self.morsechart.items():
                    if c == morse:
                        word += str(alpha)
            if len(words) > 0:
                ret_string += word + " "

        # print(arr)
        return ret_string

    def calibrate(self, arr):
        dits = [0, 2, 4]
        dahs = [8, 10, 12]
        pauses = [1, 3, 5, 9, 11]
        avg_pause = 0
        avg_dit = 0
        avg_dah = 0

        for x in dits:
            avg_dit += arr[x]
        avg_dit /= 3

        for x in dahs:
            avg_dah += arr[x]
        avg_dah /= 3

        for x in pauses:
            avg_pause += arr[x]
        avg_pause /= 5
        avg_pause /= 2
        avg_pause = round(avg_pause, 2)

        self.settings['space'] = arr[0]
        for x in arr:
            if x > self.settings['space']:
                self.settings['space'] = x

        self.settings['ditRange'] = [round(avg_dit-self.offset, 2), round(avg_dit+self.offset, 2)]
        self.settings['dahRange'] = [round(avg_dah - 0.07, 2)]
        self.settings['pauseRange'] = [avg_pause, self.settings['space']]

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
        print("dah: " + str(self.settings['dahRange']))
        print("pause: " + str(self.settings['pauseRange']))
        print("space: " + str(self.settings['space']))

    def to_morse_string(self, arr):
        morse_string = ""
        for x in arr:
            if self.settings['ditRange'][0] <= x <= self.settings['ditRange'][1]:
                morse_string += "."
            elif x >= self.settings['dahRange'][0]:
                morse_string += "-"
            else:
                if x < self.settings['ditRange'][0]:
                    morse_string += '.'
                elif x > self.settings['ditRange'][1]:
                    morse_string += "-"

        return morse_string
