
from calibration_cv import calibrate
from main_cv import morse_parser
from morse import morse
if __name__ == '__main__':
    input("You have entered calibration mode -- press any key to continue")
    mainDecoder = morse()
    calibrate(mainDecoder)
    mainDecoder.print_calib_results()
    input("Press stuff to enter parsing mode!")
    morse_parser(mainDecoder)