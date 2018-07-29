
from calibration_cv import calibrate
from main_cv import morse_parser
from morse_utills import Morse
if __name__ == '__main__':
    mainDecoder = Morse()
    print("WELCOME TO MORSE PARSER!")
    calib_mode = mainDecoder.is_calibrated() == 'n'
    while 1:
        if calib_mode:
            input("You have entered calibration mode -- press ENTER to continue")
            calibrate(mainDecoder)
            mainDecoder.print_calib_results()
            mainDecoder.save_calibration()
            calib_mode = False;
        else:
            response = input("Press ENTER to start decoding, type C to calibrate, type Q to quit ")
            if response == "":
                print("press ESCAPE on window to quit decoder")
                morse_parser(mainDecoder)
            elif response.lower() == 'c':
                calib_mode = True;
            elif response.lower() == 'q':
                break
            else:
                print("Error: Invalid Input!")


