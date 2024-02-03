from tkinter import Tk, Label, Button, Scale, HORIZONTAL, Listbox, END, Frame, StringVar, PhotoImage
from automation_system import *


class GuiController:
    def __init__(self, automation_system):
        self.light_status_label_text = None
        self.thermostat_status_label_text = None
        self.camera_status_label_text = None
        self.automation_rule_label = None
        self.camera_status_label = None
        self.toggle_camera_button = None
        self.random_motion_button = None
        self.camera_frame = None
        self.thermostat_status_label = None
        self.toggle_thermostat_button = None
        self.thermostat_temperature_scale = None
        self.thermostat_frame = None
        self.light_status_label = None
        self.toggle_light_button = None
        self.light_brightness_scale = None
        self.light_frame = None
        self.status_listbox = None
        self.window = Tk()
        self.window.title("Smart Home Dashboard")
        icon = PhotoImage(file="smart_home.png")
        self.window.iconphoto(True, icon)
        # self.window.geometry("400x300")  # Adjust as necessary
        self.window.resizable(False, False)
        self.automation_system = automation_system
        self.setup_gui()

    def setup_gui(self):
        # Status Listbox
        self.status_listbox = Listbox(self.window, width=80, relief="solid")
        self.status_listbox.pack(fill="x", padx=10, pady=10)

        # Light Control Frame
        self.light_frame = Frame(self.window)
        self.light_frame.pack(fill="x", padx=10, pady=5)
        Label(self.light_frame, text="Living Room Light Brightness").pack()
        self.light_brightness_scale = Scale(self.light_frame, from_=0, to=100, orient=HORIZONTAL,
                                            command=self.adjust_brightness)
        self.light_brightness_scale.pack()
        self.toggle_light_button = Button(self.light_frame, text="Toggle ON/OFF",
                                          command=lambda: self.toggle_device('light'))
        self.toggle_light_button.pack()
        self.light_status_label_text = StringVar()
        self.light_status_label_text.set("Living Room Brightness - 0%")
        self.light_status_label = Label(self.light_frame, textvariable=self.light_status_label_text)
        self.light_status_label.pack()

        # Thermostat Control Frame
        self.thermostat_frame = Frame(self.window)
        self.thermostat_frame.pack(fill="x", padx=10, pady=5)
        Label(self.thermostat_frame, text="Living Room Thermostat Temperature").pack()
        self.thermostat_temperature_scale = Scale(self.thermostat_frame, from_=15, to=30, orient=HORIZONTAL,
                                                  command=self.adjust_temperature)
        self.thermostat_temperature_scale.pack()
        self.toggle_thermostat_button = Button(self.thermostat_frame, text="Toggle ON/OFF",
                                               command=lambda: self.toggle_device('thermostat'))
        self.toggle_thermostat_button.pack()
        self.thermostat_status_label_text = StringVar()
        self.thermostat_status_label_text.set("Living Room Thermostat Temperature - 15°C")
        self.thermostat_status_label = Label(self.thermostat_frame, textvariable=self.thermostat_status_label_text)
        self.thermostat_status_label.pack()

        # Camera Control Frame
        self.camera_frame = Frame(self.window)
        self.camera_frame.pack(fill="x", padx=10, pady=5)
        Label(self.camera_frame, text="Front Door Camera Motion Detection").pack()
        self.random_motion_button = Button(self.camera_frame, text="Random Detect Motion",
                                           command=self.random_detect_motion)
        self.random_motion_button.pack()
        self.toggle_camera_button = Button(self.camera_frame, text="Toggle ON/OFF",
                                           command=lambda: self.toggle_device('camera'))
        self.toggle_camera_button.pack()
        self.camera_status_label_text = StringVar()
        self.camera_status_label_text.set("Front Door Camera - Motion: NO")
        self.camera_status_label = Label(self.camera_frame, textvariable=self.camera_status_label_text)
        self.camera_status_label.pack()

        # Automation Rule Label
        self.automation_rule_label = Label(self.window,
                                           text="Automation Rules: \nTurn on lights when motion is detected\n"
                                                "Turn on the infrared when the lights are off\n"
                                                "Turn off the infrared when the lights are on\n"
                                                "Camera may or may not record even the camera is on")
        self.automation_rule_label.pack(pady=10)

    def update_device_status(self):
        light = self.automation_system.devices['light']
        thermostat = self.automation_system.devices['thermostat']
        camera = self.automation_system.devices['camera']

        # Update statuses based on the rules
        self.automation_system.execute_automation_rules()

        # Clear the listbox before updating
        self.status_listbox.delete(0, END)

        # Update the status for the light
        light_status = 'On' if light.status == Status.ON else 'Off'
        brightness_display = light.brightness if light.status == Status.ON else 0
        self.status_listbox.insert(END, f"Living Room Light: SmartLight Status: {light_status}")
        self.light_status_label_text.set(f"Living Room Light - {brightness_display}%")
        self.light_brightness_scale.set(brightness_display)

        # Update the status for the thermostat
        thermostat_status = 'On' if thermostat.status == Status.ON else 'Off'
        self.status_listbox.insert(END,
                                   f"Living Room Thermostat: Thermostat Status: {thermostat_status}")
        self.thermostat_status_label_text.set(f"Living Room Thermostat - {thermostat.temperature}°C")
        self.thermostat_temperature_scale.set(thermostat.temperature)

        # Update the status for the camera
        camera_status = 'On' if camera.status == Status.ON else 'Off'
        motion_status = 'YES' if camera.motion_detected else 'NO'
        infrared_status = 'On' if camera.infrared else 'Off'
        recording_status = 'Recording' if camera.recording else 'Not Recording'
        self.status_listbox.insert(END,
                                   f"Front Door Camera: SecurityCamera Status: {camera_status}")
        self.camera_status_label_text.set(
            f"Front Door Camera - Motion: {motion_status}\n Infrared: {infrared_status}\n{recording_status}")

    def toggle_device(self, device_type):
        # Toggle the status of a device
        device = self.automation_system.devices[device_type]
        if device.status == Status.ON:
            device.turn_off()
        else:
            device.turn_on()

        self.update_device_status()

    def adjust_brightness(self, value):
        # Adjust the brightness of the light
        light = self.automation_system.devices['light']
        brightness_value = int(value)
        light.set_brightness(brightness_value)

        # Automatically turn off the light if the brightness is set to 0
        if brightness_value == 0:
            light.turn_off()
        # Automatically turn on the light if the brightness is set above 0 and the light is currently off
        elif light.status == Status.OFF:
            light.turn_on()
        self.update_device_status()

    def adjust_temperature(self, value):
        # Adjust the temperature of the thermostat
        thermostat = self.automation_system.devices['thermostat']
        thermostat.set_temperature(int(value))
        self.update_device_status()

    def random_detect_motion(self):
        # Randomly simulate motion detection
        camera = self.automation_system.devices['camera']
        camera.motion_detected = not camera.motion_detected  # This attribute should be handled by your SecurityCamera class
        self.update_device_status()

    def run(self):
        self.update_device_status()  # Initial update
        self.window.mainloop()
