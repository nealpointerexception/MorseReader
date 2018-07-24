
from calibration_cv import calibrate
from main_cv import morse_parser
from morse_utills import morse
if __name__ == '__main__':
    mainDecoder = morse()
    if mainDecoder.is_calibrated() == 'n':
        input("You have entered calibration mode -- press any key to continue")
        calibrate(mainDecoder)
        mainDecoder.print_calib_results()
        mainDecoder.save_calibration()

    input("Press stuff to enter parsing mode!")
    morse_parser(mainDecoder)