from abc import ABC


class Status:
    OFF = 0
    ON = 1


class IoTDevice(ABC):
    """ Base class for IoT devices. """

    def __init__(self, device_id):
        self.device_id = device_id
        self.status = Status.OFF

    def turn_on(self):
        self.status = Status.ON

    def turn_off(self):
        self.status = Status.OFF


class SmartLight(IoTDevice):
    """ Smart Light with brightness control. """

    def __init__(self, device_id):
        super().__init__(device_id)
        self.brightness = 0

    def set_brightness(self, brightness):
        if 0 <= brightness <= 100:
            self.brightness = brightness


class Thermostat(IoTDevice):
    """ Thermostat with temperature control. """

    def __init__(self, id):
        super().__init__(id)
        self.temperature = 15

    def set_temperature(self, temperature):
        if 15 <= temperature <= 30:
            self.temperature = temperature


class SecurityCamera(IoTDevice):
    """ Security Camera with infrared and recording"""

    def __init__(self, device_id):
        super().__init__(device_id)
        self.infrared = False
        self.recording = False
        self.motion_detected = False

    def toggle_infrared(self):
        self.infrared = not self.infrared

    def toggle_recording(self):
        self.recording = not self.recording
