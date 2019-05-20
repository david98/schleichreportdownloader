from gui import UiMainWindow, QtWidgets
from schleichore import TestingDevice, TestManager

import logging
import sys
from serial import SerialException


# searches for the device on the first 100 USB-RS232 adapters
# returns a list of tuples like ('/dev/ttyUSB1', id_string)
def get_devices():
    base_serial_string = "/dev/ttyUSB"
    devices = []
    i = -1
    while i < 100:
        try:
            i += 1
            device = TestingDevice(base_serial_string + str(i))
            id_string = device.identify()
            # this may need to be improved by actually checking the response
            if len(id_string) > 0:
                devices.append((base_serial_string + str(i), id_string))
        except SerialException:
            continue
        except Exception:
            logging.exception('Unknown exception while searching for testing device.')
    return devices


def init_app():
    # logging configuration
    log_levels = {
        1: logging.DEBUG,
        2: logging.INFO,
        3: logging.WARNING,
        4: logging.ERROR,
        5: logging.CRITICAL
    }
    desired_log_level_index = 3
    try:
        desired_log_level_index = int(sys.argv[1])
    except IndexError:
        pass

    log_config = {
        'level': log_levels[desired_log_level_index]
    }

    logging.basicConfig(**log_config)
    # end logging configuration

    app = QtWidgets.QApplication(sys.argv)
    available_devices = get_devices()
    if len(available_devices) == 0:
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.showMessage('No connected device available. Exiting.')
        sys.exit(app.exec_())
    else:
        main_window = QtWidgets.QMainWindow()
        device = TestingDevice(available_devices[0][0])

        # we need to flush the device's cache, otherwise we'll get an old report
        # maybe we could ask the user if he wants to store these
        device.get_all_reports()

        test_manager = TestManager(device, log_config)
        ui = UiMainWindow(test_manager, log_config)
        ui.setup_ui(main_window)
        main_window.showFullScreen()
        # this code should not be here, but I couldn't find a better way to do this
        ui.startup.emit(1)
        if ui.test_manager.please_resume:
            ui.action_start_test.trigger()
        sys.exit(app.exec_())


if __name__ == "__main__":
    init_app()
