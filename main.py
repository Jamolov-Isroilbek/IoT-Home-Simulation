import threading
import time
from automation_system import *
from iothings_gui import GuiController


def start_simulation(system, gui_controller):
    while True:
        system.simulate_device_behavior()
        system.execute_automation_rules()

        # Schedule the GUI update on the main thread
        # gui_controller.update_device_status()
        gui_controller.window.after(0, gui_controller.update_device_status)
        time.sleep(3)  # Update every 3 seconds


# Initialize the automation system
automation_system = AutomationSystem()

# Add devices to the system
automation_system.add_device('light', SmartLight('Light1'))
automation_system.add_device('thermostat', Thermostat('Thermo1'))
automation_system.add_device('camera', SecurityCamera('Camera1'))

# Initialize GUI controller
gui_controller = GuiController(automation_system)

# Start the simulation in a separate thread
simulation_thread = threading.Thread(target=start_simulation, args=(automation_system, gui_controller))
simulation_thread.daemon = True
simulation_thread.start()

# Run the GUI
gui_controller.run()
