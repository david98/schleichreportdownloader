# coding=UTF-8

import serial
import time
import datetime


class TestReport:

    def __init__(self, report_string):
        result = report_string.split('NUM_1')
        test_info = result[1].split(' ')
        self.name = test_info[1].replace('NAME_', '').replace('*', ' ')
        date_string = test_info[2].replace('DA_', '').replace('_', ' ')
        self.date = datetime.datetime.strptime(date_string, '%d.%m.%y %H:%M:%S')
        steps = list(map(lambda step: step.split(' '), result[0].split('CH')))
        self.steps_with_results = []
        for idx, step in enumerate(steps):
            if idx == 0:
                del step[0]
            else:
                del step[0:2]
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

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB1', baudrate=9600, timeout=None, parity=serial.PARITY_NONE,
                                 bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, xonxoff=False)

    def send_custom_command(self, command_hex):
        self.ser.write(serial.to_bytes(command_hex))

    def read_all(self):
        return self.ser.read(self.ser.inWaiting())

    def beep(self):
        self.send_custom_command(TestingDevice.BEEP_COMMAND)
        time.sleep(0.12)

    def identify(self):
        self.send_custom_command(TestingDevice.IDENTIFY_COMMAND)
        time.sleep(0.12)
        return self.read_all()

    def get_report(self):
        self.send_custom_command(TestingDevice.GET_REPORT_COMMAND)
        time.sleep(2)
        result = self.read_all()
        if len(result.strip().replace(b'\x15', b'').replace(b'4', b'').replace(b'\x03', b'').replace(b'2', b'')) == 0:
            raise Exception('No report available for download.')
        return TestReport(result)

    def close_communication(self):
        self.ser.close()


device = TestingDevice()
#for i in range(0, 1):
#    device.beep()
device.beep()
print(device.identify())
print(device.get_report())
#report = TestReport("��001 HV 1200 100.00 1206 0.50 IO_61.0_Tutto*vs*Massa*CH 002 HV 1200 100.00 1209 0.41 IO_61.0_L1l1*vs*altri*CH 003 HV 1200 100.00 1213 0.42 IO_61.0_L2l2*vs*altri*CH 004 HV 1200 100.00 1212 0.44 IO_61.0_L3l3*vs*altri*CH 005 HV 1200 100.00 1209 0.44 IO_61.0_Line*vs*Load*AP NUM_1 NAME_UL98*600V DA_15.04.19_10:41:27 xE0 END 55")
#print(report)
device.close_communication()
