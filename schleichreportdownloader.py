# coding=UTF-8

import serial
import time
import datetime
import progressbar

from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font


def as_text(value):
    if value is None:
        return ""
    return str(value)


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
        wb = Workbook()

        bold_font = Font(bold=True)

        dest_filename = name + '.xlsx'

        ws1 = wb.active
        ws1.title = "Test Report"

        ws1['A1'] = 'Preset Name'
        ws1['B1'] = 'Date'
        ws1['A1'].font = bold_font
        ws1['B1'].font = bold_font

        ws1['A2'] = self.name
        ws1['B2'] = self.date

        ws1['A4'] = 'Step Number'
        ws1['B4'] = 'Method'
        ws1['C4'] = 'Step Name'
        ws1['D4'] = 'Limit Value'
        ws1['E4'] = 'Actual Value'
        ws1['F4'] = 'Test Condition'
        ws1['G4'] = 'Actual Condition'
        ws1['H4'] = 'Test Duration'
        ws1['I4'] = 'Go'

        ws1['A4'].font = bold_font
        ws1['B4'].font = bold_font
        ws1['C4'].font = bold_font
        ws1['D4'].font = bold_font
        ws1['E4'].font = bold_font
        ws1['F4'].font = bold_font
        ws1['G4'].font = bold_font
        ws1['H4'].font = bold_font
        ws1['I4'].font = bold_font

        row = 5
        for step in self.steps_with_results:
            for col in range(1, len(step) + 2):
                value = 0
                if col == 1:
                    value = row - 4
                if col == 2:
                    value = step['method']
                elif col == 3:
                    value = step['name']
                elif col == 4:
                    value = str(step['limit_value']) + ' mA'
                elif col == 5:
                    value = str(step['actual_value']) + ' mA'
                elif col == 6:
                    value = str(step['test_condition']) + ' V'
                elif col == 7:
                    value = str(step['actual_condition']) + ' V'
                elif col == 8:
                    value = str(step['test_duration']) + ' s'
                elif col == 9:
                    value = step['go']
                _ = ws1.cell(column=col, row=row, value=value)
            row += 1

        column_widths = []
        for row in ws1.iter_rows():
            for i, cell in enumerate(row):
                try:
                    column_widths[i] = max(column_widths[i], len(as_text(cell.value)))
                except IndexError:
                    column_widths.append(len(as_text(cell.value)))

        for i, column_width in enumerate(column_widths):
            ws1.column_dimensions[get_column_letter(i + 1)].width = column_width + 5

        wb.save(filename=dest_filename)

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
        self.send_custom_command
            time.sleep(0.12)
        return read_data
(TestingDevice.GET_REPORT_COMMAND)
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
#report = TestReport("��001 HV 1320 100.00 1338 0.58 IO_61.0_Tutto*vs*Massa*CH 002 HV 1320 100.00 1326 0.31 IO_61.0_Potenza*vs*Circ.Secondari*CH 003 HV 1320 100.00 1337 0.41 IO_61.0_Nn*vs*altri*CH 004 HV 1320 100.00 1328 0.40 IO_61.0_L1l1*vs*altri*CH 005 HV 1320 100.00 1339 0.42 IO_61.0_L2l2*vs*altri*CH 006 HV 1320 100.00 1328 0.44 IO_61.0_L3l3*vs*altri*CH 007 HV 900 100.00 921 0.19 IO_61.0_Circ.Secondari*vs*Massa*CH 008 HV 1320 100.00 1339 0.51 IO_61.0_Line*vs*Load*AP 009 HV 1320 100.00 1335 0.55 IO_61.0_Tutto*vs*Massa*AP 010 HV 1320 100.00 1325 0.31 IO_61.0_Potenza*vs*Circ.Secondari*AP 011 HV 900 100.00 907 0.19 IO_61.0_Circ.Secondari*vs*Massa*AP 012 HV 600 100.00 614 0.16 IO_61.0_Motore*vs*Massa NUM_1 NAME_ANSI*635V*508V*252V*60% DA_15.04.19_12:21:10 xE2 END 73 ANSI 635V 508V 252V 60% | 2019-04-15 12:21:10")
#report.store_as_xlsx('example')
report = None
print('Waiting for report...')
bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
i = 0
while not report:
    try:
        report = device.get_first_available_report()
        report.store_as_xlsx('report')
    except NoReportException:
        i += 1
        bar.update(i)
        time.sleep(0.5)
device.close_communication()
