import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service
import logging
import subsystem_connection # this is where the sensors and control systems put their output
import time
import watchdog.events
import watchdog.observers

# Import classes from backend
from RSSBLEBackend import (
    adapter_setup,
    Advertisement,
    Application,
    Characteristic,
    Service
)


# Import MainLoop to manage system events
MainLoop = None
from gi.repository import GLib  # for Python 3
MainLoop = GLib.MainLoop

# Logging for system events
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logHandler = logging.StreamHandler()
filelogHandler = logging.FileHandler("logs.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logHandler.setFormatter(formatter)
filelogHandler.setFormatter(formatter)
logger.addHandler(filelogHandler)
logger.addHandler(logHandler)

mainloop = None  # no mainloop to start (global version)

# Error exceptions using DBus exceptions

class InvalidArgsException(dbus.exceptions.DBusException):
    _dbus_error_name = "org.freedesktop.DBus.Error.InvalidArgs"


class NotSupportedException(dbus.exceptions.DBusException):
    _dbus_error_name = "org.bluez.Error.NotSupported"


class NotPermittedException(dbus.exceptions.DBusException):
    _dbus_error_name = "org.bluez.Error.NotPermitted"


class InvalidValueLengthException(dbus.exceptions.DBusException):
    _dbus_error_name = "org.bluez.Error.InvalidValueLength"


class FailedException(dbus.exceptions.DBusException):
    _dbus_error_name = "org.bluez.Error.Failed"

def register_app_cb():
    logger.info("GATT application registered")


def register_app_error_cb(error):
    logger.critical("Failed to register application: " + str(error))
    mainloop.quit()


# Class for Robotic Sorting System service
class RSSService(Service):
    RSS_UUID = "4f5a4acc-6434-4d33-a791-589fdca0daf5"

    # Set initial values and add characteristics
    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.RSS_UUID, True)
        # self.add_characteristic(ConfigurationWriteCharacteristic(bus, 0, self))
        # self.add_characteristic(WeightSensorReadCharacteristic(bus, 1, self))

# Class for the configuration read/write characteristic
class ConfigurationWriteCharacteristic(Characteristic):
    uuid = "89097689-8bc2-44cb-9142-f17c71ed24f8"  # Randomly generated

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index, self.uuid, ["read", "write"], service,
        )

        # Initial value
        self.value = dbus.Array([subsystem_connection.config[0], subsystem_connection.config[1], subsystem_connection.config[2], subsystem_connection.config[3]], signature='ay')  # ay specifies an array of bytes

    # Handle read
    def ReadValue(self, options):
        logger.debug("Configuration read as: " + repr(self.value))  # repr: printable version of self.value
        return self.value

    # Handle write (can add input checking here)
    def WriteValue(self, value, options):
        writeval = dbus.Array(value, signature='ay')
        logger.debug("Writing configuration as: " + repr(writeval))
        self.value = writeval


class WeightSensorReadCharacteristic(Characteristic):
    uuid = "4f5641bf-1119-4d1f-932d-fff7840ddc02"

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index, self.uuid, ["read"], service,  # Note that this is read-only
        )

        # Initial value
        self.value = [subsystem_connection.weight[0], subsystem_connection.weight[1], subsystem_connection.weight[2]]

    # Handle read
    def ReadValue(self, options):
        logger.debug("Weight read as: " + repr(self.value))
        return self.value
        
    # Handle write (from sensors)
    def WriteValue(self, value, options):
        writeval = dbus.Array(value, signature='ay')
        logger.debug("Size written from sensors as: " + repr(writeval))
        self.value = writeval

# Class that defines the desired advertisement characteristics for the Robotic Sorting System
class RSSAdvertisement(Advertisement):
    def __init__(self, bus, index):
        Advertisement.__init__(self, bus, index, "peripheral")
        # Advertise UUID for service
        self.add_service_uuid(RSSService.RSS_UUID)
        # Advertise local name for identification
        self.add_local_name("Robotic Sorting System")
        self.include_tx_power = True

# Class for watchdog observer
class Handler(watchdog.events.FileSystemEventHandler):
    def on_modified(self, event):
        print('Subsystem connection changed')
        # TODO: make this update the weight char. value

def main():
    # Watch for changes with watchdog
    path = '/home/lifeofpi/BLEProject/'
    event_handler = Handler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=path, recursive=False)
    observer.start()
    try:
        while True:
            logger.info("Entered main")
            global mainloop
            dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)  # Connects global mainloop to actual system MainLoop
            # Get system DBus
            bus = dbus.SystemBus()
            # Attach system Bluetooth adapter to the variable adapter
            adapter = adapter_setup(bus)
            adapter_obj = bus.get_object("org.bluez", adapter)
            # Attach properties of the adapter to "adapter_props"
            adapter_props = dbus.Interface(adapter_obj, "org.freedesktop.DBus.Properties")
            # Set the "Powered" property of the adapter to turn on Bluetooth
            adapter_props.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))
            
            # Set the org.bluez.LEAdvertisingManager1 property to advertise the right information
            # Assign variable to advertisement manager and service manager
            ad_manager = dbus.Interface(adapter_obj, "org.bluez.LEAdvertisingManager1")
            service_manager = dbus.Interface(adapter_obj, "org.bluez.GattManager1")
            # Create advertisement in D-Bus
            advertisement = RSSAdvertisement(bus, 0)
            # Register advertisement with BlueZ
            ad_manager.RegisterAdvertisement(
                advertisement.get_path(),
                {},
                reply_handler=register_app_cb,
                error_handler=register_app_error_cb
            )
            # Create application and add service + characteristics
            app = Application(bus)
            rssService = RSSService(bus, 2)  # Gives this instance of the service its own variable for later modification
            weightChar = WeightSensorReadCharacteristic(bus, 0, rssService) # Same with characteristics
            configChar = ConfigurationWriteCharacteristic(bus, 1, rssService)
            rssService.add_characteristic(weightChar)
            rssService.add_characteristic(configChar)
            app.add_service(rssService) # Add the RSS service to the started application
            service_manager = dbus.Interface(adapter_obj, "org.bluez.GattManager1")
            service_manager.RegisterApplication(
                app.get_path(),
                {},
                reply_handler = register_app_cb,
                error_handler = [register_app_error_cb]
            )
            # Tie into main loop
            mainloop = MainLoop()
            mainloop.run()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Connect to main
if __name__ == "__main__":
    main()

