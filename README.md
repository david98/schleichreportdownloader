# WTF is this?

This program was made to replace the software provided with Schleich's GLP2-e, a device for dielectric withstand tests.
It allows an operator to start a test with the currently selected test program and then save the report as an .xlsx file.
It's meant to be used as a control panel in conjunction with a Raspberry Pi and a touchscreen, but
it runs just fine on any Linux machine (it could be made to work with other OS' and I plan
on doing it in the future).

# Requirements
* Python 3.7+
* PiP

# Setup

1. Clone this repository.
2. Move into the cloned repository and run `pip install -r requirements.txt`.<br>
You may encounter some issues when installing PyQT on Raspberry Pi OS. If so, follow these steps:
    1. Open `requirements.txt`, then remove `PyQt5==5.12.1`, `PyQt5-sip==4.19.17` and `PyQt5-stubs==5.12.1.0`
    2. Run: 
    ```
        $ sudo apt install python3-pyqt5
     ```
    3. Run once again `pip install -r requirements.txt`

# Configuration

The configuration file, named `configuration.ini` resides in the repository root.

You can pass in a directory path as the first command line argument. If the path exists,
it will be used as the working directory for the program.
