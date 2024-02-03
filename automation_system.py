from iothings import *
import random


class AutomationSystem:
    """ Manages IoT devices and their interactions. """

    def __init__(self):
        self.devices = {'light': None, 'thermostat': None, 'camera': None}

    def add_device(self, device_type, device):
        self.devices[device_type] = device

    def execute_automation_rules(self):
        """ Execute automation rules based on device states. """
        light = self.devices['light']
        camera = self.devices['camera']

        # Rule for infrared: If light is off, infrared is on; otherwise, it's off
        if light.status == Status.OFF:
            camera.infrared = True
        else:
            camera.infrared = False

        # Rule for recording: Randomly toggle recording on/off
        if camera.status == Status.ON:
            camera.recording = random.choice([True, False])
        else:
            camera.recording = False

        # Rule for turning on the light when motion is detected
        if camera.motion_detected and not light.status:
            light.turn_on()

    def simulate_device_behavior(self):
        """ Randomly changes the state of devices. """
        for device in self.devices.values():
            if device:
                if random.random() < 0.5:
                    device.turn_on()
                else:
                    device.turn_off()

                if isinstance(device, SmartLight):
                    device.set_brightness(random.randint(0, 100))
                elif isinstance(device, Thermostat):
                    device.set_temperature(random.randint(15, 30))
