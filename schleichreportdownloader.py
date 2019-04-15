# coding=UTF-8

import serial
import time
import datetime
import progressbar


class NoReportException(Exception):
    pass


class TestReport:

    def __init__(self, report_string):
        result = report_string.split('NUM_1')
        test_info = result[1].split(' ')
        self.name = test_info[1].replace('NAME_', '').replace('*', ' ')
        date_string = test_info[2].replace('DA_', '').replace('_', ' ')
        self.date = datetime.datetime.strptime(date_string, '%d.%m.%y %H:%M:%S')
        elements = result[0].split(' ')
        steps = [elements[n:n + 7] for n in range(0, len(elements), 7)]
        self.steps_with_results = []
        for step in steps:
            if len(step) > 1:
                del step[0]
                split_step_info = step[5].split('_')
                parsed_step = {
                    'name': split_step_info[2].replace('*', ' '),
                    'method': step[0],
                    'test_condition': float(step[1]),
                    'limit_value': float(step[2]),
                    'actual_condition': float(step[3]),
                    'actual_value': float(step[4]),
                    'test_duration': float(split_step_info[1]),
                }
                parsed_step['go'] = 'GO' if parsed_step['actual_value'] <= parsed_step['limit_value'] else 'NGO'
                self.steps_with_results.append(parsed_step)

    def store_as_xlsx(self, name):
        pass

    def __str__(self):
        string = ''
        string += self.name + ' | ' + str(self.date) + '\n'
        for idx, step in enumerate(self.steps_with_results):
            string += str(step) + '\n'
        return string


class TestingDevice:

    BEEP_COMMAND = [0x02, 0x81, 0xfa, 0x62, 0x20, 0x33, 0x42, 0x03]
    IDENTIFY_COMMAND = [0x02, 0x81, 0xfd]
    GET_REPORT_COMMAND = [0x02, 0x81, 0x06]
    START_TEST_COMMAND = [0x02, 0x81, 0xfa, 0x73, 0x20, 0x32, 0x41, 0x03]

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB1', baudrate=9600, timeout=None, parity=serial.PARITY_NONE,
                                 bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, xonxoff=False)

    def send_custom_command(self, command_hex):
        self.ser.write(serial.to_bytes(command_hex))
        time.sleep(0.12)

    def read_all(self):
        read_data = ''
        while self.ser.in_waiting > 0:
            try:
                new_data = self.ser.read(self.ser.in_waiting)
                read_data += new_data.decode(errors='ignore')
            except TypeError:
                continue
            time.sleep(0.12)
        return read_data

    def beep(self):
        self.send_custom_command(TestingDevice.BEEP_COMMAND)

    def identify(self):
        self.send_custom_command(TestingDevice.IDENTIFY_COMMAND)
        return self.read_all()

    def get_first_available_report(self):
        self.send_custom_command(TestingDevice.GET_REPORT_COMMAND)
        result = self.read_all()
        if len(result.strip().replace('\x07', '').replace('\x15', '').replace('4', '').replace('\x03', '').replace('2', '')) == 0:
            raise NoReportException('No report available for download.')
        return TestReport(result)

    def get_all_reports(self):
        reports = []
        while True:
            try:
                reports.append(self.get_first_available_report())
            except NoReportException:
                return reports

    def start_test(self):
        self.send_custom_command(TestingDevice.START_TEST_COMMAND)
        self.ser.reset_input_buffer()

    def clear_all_reports(self):
        self.get_all_reports()

    def close_communication(self):
        self.ser.close()


device = TestingDevice()
device.start_test()
report = None
print('Waiting for report...')
bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
i = 0
while not report:
    try:
        report = device.get_first_available_report()
    except NoReportException:
        i += 1
        bar.update(i)
        time.sleep(0.5)
device.close_communication()
