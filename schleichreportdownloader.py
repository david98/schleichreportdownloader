import logging
import os
import sys

from serial import SerialException
from configparser import ConfigParser

from custom_libs.gui import UiMainWindow, QtWidgets
from custom_libs.schleichore import TestingDevice, TestManager


class Configuration:

    DEFAULT_CONFIG_FILE_NAME = 'default-configuration.ini'
    CONFIG_FILE_NAME = 'configuration.ini'
    LOGS_FOLDER = 'logs'
    LOG_NAME = 'logging-file.log'
    LOG_LEVELS = {
        1: logging.DEBUG,
        2: logging.INFO,
        3: logging.WARNING,
        4: logging.ERROR,
        5: logging.CRITICAL
    }

    def __init__(self):
        parser = ConfigParser()

        '''If a configuration file was not created by the user, we create a default one.
        This is to allow updates to the default configuration without breaking the user one, since the latter won't be
        tracked by git '''
        if not os.path.exists(self.CONFIG_FILE_NAME):
            try:
                with open(self.DEFAULT_CONFIG_FILE_NAME) as f:
                    lines = f.readlines()
                    with open(self.CONFIG_FILE_NAME, "w") as f1:
                        f1.writelines(lines)
            except IOError:
                print('Exception while creating a configuration file. Maybe default-configuration.ini was deleted?')
                exit(1)

        parser.read(self.CONFIG_FILE_NAME)

        try:

            if not os.path.exists(self.LOGS_FOLDER):
                os.makedirs(self.LOGS_FOLDER)

            log_level = int(parser.get('logging', 'level', fallback=3))
            self.log_config = {
                'level': self.LOG_LEVELS[log_level],
                'format': '%(asctime)s - [%(levelname)s] - %(message)s',
                'datefmt': '%d-%b-%y %H:%M:%S',
                'filename': f'{self.LOGS_FOLDER}/{self.LOG_NAME}',
                'filemode': 'a'
            }

            self.default_reports_folder = parser.get('reports', 'default_folder', fallback='./')

        except ValueError:
            print('Unexpected value in configuration file. Quitting.')
            exit(1)


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

    # we need to change the current working directory to the one passed as a command line argument, if present
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if os.path.exists(path):
            os.chdir(path)

    config = Configuration()

    logging.basicConfig(**config.log_config)
    logging.debug('Log file test.')

    app = QtWidgets.QApplication(sys.argv)
    screen_geometry = app.desktop().screenGeometry()
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

        test_manager = TestManager(device, config.log_config)
        ui = UiMainWindow(test_manager, config)
        ui.setup_ui(main_window, screen_geometry)
        main_window.showFullScreen()
        # this code should not be here, but I couldn't find a better way to do this
        ui.startup.emit(1)
        if ui.test_manager.please_resume:
            ui.action_start_test.trigger()
        sys.exit(app.exec_())


if __name__ == "__main__":
    init_app()
