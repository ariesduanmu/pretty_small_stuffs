class color_print:
    def __init__(self):
        self.out = ""

    def output(self):
       print("{}\033[0m".format(self.out))

def set_attr():
    def _add(name, number):
        def inner(self, addition=""):
            self.out += '\033[{:d}m{}'.format(number, addition)
            return self
        setattr(color_print, name, inner)

    colors = {
        'raw': 0,
        'bold': 1,
        'dim': 2,
        'underlined': 4,
        'blinking': 5,
        'inverted': 7,
        'hidden': 8,
        'black': 30,
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'magenta': 35,
        'cyan': 36,
        'light_gray': 37,
        'black_bg': 40,
        'red_bg': 41,
        'green_bg': 42,
        'yellow_bg': 43,
        'blue_bg': 44,
        'purple_bg': 45,
        'cyan_bg': 46,
        'gray_bg': 47,
        'dark_gray': 90,
        'light_red': 91,
        'light_green': 92,
        'light_yellow': 93,
        'light_blue': 94,
        'light_magenta': 95,
        'light_cyan': 96,
        'white': 97,
        'dark_gray_bg': 100,
        'light_red_bg': 101,
        'light_green_bg': 102,
        'light_yellow_bg': 103,
        'light_blue_bg': 104,
        'light_purple_bg': 105,
        'light_cyan_bg': 106,
        'white_bg': 107
    }

    for item in colors.items():
         if len(item) > 1:
             _add(item[0],item[1])

set_attr()

def test():
    color_print().red("Hello").output()
    color_print().green("world").output()

if __name__ == "__main__":
    test()

