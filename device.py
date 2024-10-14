from uuid import UUID

from pygatt import GATTToolBackend

ADDRESS = "80:EA:CA:89:5F:EA"

handles = {
    0x3: UUID("00002a00-0000-1000-8000-00805f9b34fb"),
    0x5: UUID("00002a01-0000-1000-8000-00805f9b34fb"),
    0x7: UUID("00002a02-0000-1000-8000-00805f9b34fb"),
    0x9: UUID("00002a04-0000-1000-8000-00805f9b34fb"),
    0xe: UUID("00002a05-0000-1000-8000-00805f9b34fb"),
    0x12: UUID("00000001-0000-1000-8000-00805f9b34fb"),
    0x15: UUID("00000002-0000-1000-8000-00805f9b34fb"),
    0x17: UUID("00000004-0000-1000-8000-00805f9b34fb"),
    0x19: UUID("00000007-0000-1000-8000-00805f9b34fb"),
    0x1b: UUID("00000010-0000-1000-8000-00805f9b34fb"),
    0x1d: UUID("00000013-0000-1000-8000-00805f9b34fb"),
    0x1f: UUID("00000014-0000-1000-8000-00805f9b34fb"),
    0x21: UUID("00001001-0000-1000-8000-00805f9b34fb"),
    0x25: UUID("8082caa8-41a6-4021-91c6-56f9b954cc34"),
    0x27: UUID("724249f0-5ec3-4b5f-8804-42345af08651"),
    0x29: UUID("6c53db25-47a1-45fe-a022-7c92fb334fd4"),
    0x2b: UUID("9d84b9a3-000c-49d8-9183-855b673fda31"),
    0x2d: UUID("457871e8-d516-4ca1-9116-57d0b17b9cb2"),
    0x2f: UUID("5f78df94-798c-46f5-990a-b3eb6a065c88"),
    0x33: UUID("00001a00-0000-1000-8000-00805f9b34fb"),
    0x35: UUID("00001a01-0000-1000-8000-00805f9b34fb"),
    0x38: UUID("00001a02-0000-1000-8000-00805f9b34fb"),
    0x3c: UUID("00001a11-0000-1000-8000-00805f9b34fb"),
    0x3e: UUID("00001a10-0000-1000-8000-00805f9b34fb"),
    0x41: UUID("00001a12-0000-1000-8000-00805f9b34fb"),

}
DEVICE_NAME_HANDLE = 0x03
REAL_TIME_DATA_HANDLE = 0x35
DEVICE_BATTERY_FIRMWARE = 0x38

COMMAND_MODE_HANDLE = 0x33
COMMAND_MODE_REAL_TIME_INIT = bytes([0xa0, 0x1f])


class CaptorData:
    def __init__(self, data: bytearray):
        from struct import unpack
        # we ignore the last 6 bytes
        self.temp, self.light, self.soil_fertility, self.conductivity = unpack("<HxIBH", data[:10])
        self.temp /= 10


class MyCaptorDevice:
    def __init__(self, address: str):
        self.address = address
        self.adapter = GATTToolBackend()

    @property
    def device_name(self):
        return self.read(DEVICE_NAME_HANDLE).decode()

    @property
    def version(self):
        data = self.read(DEVICE_BATTERY_FIRMWARE)
        # We remove the first byte (battery level) and the second byte (separator)
        return data[2:].decode()

    @property
    def battery(self):
        data = self.read(DEVICE_BATTERY_FIRMWARE)
        return data[0]

    def get_real_time_data(self) -> CaptorData:
        self.write(COMMAND_MODE_HANDLE, COMMAND_MODE_REAL_TIME_INIT)
        return CaptorData(self.read(REAL_TIME_DATA_HANDLE))

    def read(self, handle: hex) -> bytearray:
        try:
            self.adapter.start()
            device = self.adapter.connect(self.address)
            res = device.char_read(handles[handle])
        except Exception as e:
            print("\033[31m" + f"[ERROR] Error encountered while reading characteristic {handle}" + "\033[0m")
            res = None
        finally:
            self.adapter.stop()
        return res

    def write(self, handle: hex, data: bytearray | bytes):
        try:
            self.adapter.start()
            device = self.adapter.connect(self.address)
            device.char_write(handles[handle], data, wait_for_response=False)
        except Exception as e:
            print("\033[31m" + f"[ERROR] Error encountered while writing characteristic {handle}" + "\033[0m")
        finally:
            self.adapter.stop()




if __name__ == '__main__':
    flower_care = MyCaptorDevice(ADDRESS)
    print("Name: {}, Battery level {}, Firmware version: {}".format(flower_care.device_name,flower_care.battery,flower_care.version))
    data = flower_care.get_real_time_data()
    print("Temperature: ", data.temperature)
    print("Light: ", data.light)
    print("Moisture: ", data.moisture)
    print("Conductivity: ", data.conductivity)
