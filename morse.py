class morse():
    def __init__(self):
        self.morsechart = {'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..', 'g': '--.',
                           'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.',
                           'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.', 's': '...', 't': '-', 'u': '..-',
                           'v': '...-', 'w': '.--', 'x': '-..-', 'y': '-.--', 'z': '--..'}
        self.ditRange = []
        self.dahRange = []
        self.spaceRange = []
        self.pauseRange = []

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
            avgPause += arr[x]
        avgPause /= 5
        avgPause /= 2
        avgPause = round(avgPause, 2)

        avgSpace = arr[0]
        for x in arr:
            if x > avgSpace:
                avgSpace = x

        self.ditRange = [avgDit-self.offset, avgDit+self.offset]
        self.dahRange = [avgDah - self.offset, avgDah + self.offset]
        self.spaceRange = [avgSpace - self.offset, avgSpace + self.offset]
        self.pauseRange = [avgPause - self.offset, avgPause + self.offset]

        print("dit: " + str(avgDit))
        print("dah: " + str(avgDah))
        print("pause: " + str(avgPause))
        print("space: " + str(avgSpace))


    def to_morse_string(self, timeArr):
        maxLen = max(timeArr)
        minLen = min(timeArr)
        print(maxLen)
        print(minLen)


if __name__ == '__main__':
    morsegods = morse()
    hello = morsegods.to_morse("HELLO WORLD")
    print("HELLO WORLD: " + hello)

    helloagain = morsegods.to_alpha(hello)
    print(hello + ": " + helloagain)