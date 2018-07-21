class morse():
    def __init__(self):
        self.morsechart = {'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..', 'g': '--.',
                           'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.',
                           'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.', 's': '...', 't': '-', 'u': '..-',
                           'v': '...-', 'w': '.--', 'x': '-..-', 'y': '-.--', 'z': '--..'}

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

    def to_morse_string(self, timeArr=[]):
        pass;


if __name__ == '__main__':
    morsegods = morse()
    hello = morsegods.to_morse("HELLO WORLD")
    print("HELLO WORLD: " + hello)

    helloagain = morsegods.to_alpha(hello)
    print(hello + ": " + helloagain)