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
        time.sleep(0.12)

    def read_all(self):
        read_data = ''
        while self.ser.inWaiting() > 0:
            read_data += self.ser.read(self.ser.inWaiting())
            time.sleep(0.12)
        return read_data

    def beep(self):
        self.send_custom_command(TestingDevice.BEEP_COMMAND)

    def identify(self):
        self.send_custom_command(TestingDevice.IDENTIFY_COMMAND)
        return self.read_all()

    def get_report(self):
        self.send_custom_command(TestingDevice.GET_REPORT_COMMAND)
        result = self.read_all()
        print(result)
        if len(result.strip().replace(b'\x15', b'').replace(b'4', b'').replace(b'\x03', b'').replace(b'2', b'')) == 0:
            raise Exception('No report available for download.')
        return TestReport(result)

    def close_communication(self):
        self.ser.close()


device = TestingDevice()
#for i in range(0, 1):
#    device.beep()
#device.beep()
#print(device.identify())
#print(device.get_report())
report = TestReport("��001 HV 1320 100.00 1338 0.58 IO_61.0_Tutto*vs*Massa*CH 002 HV 1320 100.00 1326 0.31 IO_61.0_Potenza*vs*Circ.Secondari*CH 003 HV 1320 100.00 1337 0.41 IO_61.0_Nn*vs*altri*CH 004 HV 1320 100.00 1328 0.40 IO_61.0_L1l1*vs*altri*CH 005 HV 1320 100.00 1339 0.42 IO_61.0_L2l2*vs*altri*CH 006 HV 1320 100.00 1328 0.44 IO_61.0_L3l3*vs*altri*CH 007 HV 900 100.00 921 0.19 IO_61.0_Circ.Secondari*vs*Massa*CH 008 HV 1320 100.00 1339 0.51 IO_61.0_Line*vs*Load*AP 009 HV 1320 100.00 1335 0.55 IO_61.0_Tutto*vs*Massa*AP 010 HV 1320 100.00 1325 0.31 IO_61.0_Potenza*vs*Circ.Secondari*AP 011 HV 900 100.00 907 0.19 IO_61.0_Circ.Secondari*vs*Massa*AP 012 HV 600 100.00 614 0.16 IO_61.0_Motore*vs*Massa NUM_1 NAME_ANSI*635V*508V*252V*60% DA_15.04.19_12:21:10 xE2 END 73 ANSI 635V 508V 252V 60% | 2019-04-15 12:21:10")
print(report)
device.close_communication()
