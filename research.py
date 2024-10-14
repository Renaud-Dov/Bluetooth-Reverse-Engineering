from time import sleep
from uuid import UUID

import pygatt
from pygatt import GATTToolBackend
from pygatt.backends.gatttool.device import GATTToolBLEDevice

adapter = GATTToolBackend()
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

DEVICE_NAME = 0x03
COMMAND_MODE = 0x33
REAL_TIME_DATA = 0x35


def scan_bluetooth_devices():
    try:
        adapter.start()
        devices = adapter.scan()
        for device in devices:
            print("Found BLE device: ", device["address"], device["name"])
    finally:
        adapter.stop()

def read_characteristic(device, uuid) -> bytearray:
    try:
        return device.char_read(uuid)
    except Exception as e:
        print("\033[31m" + f"[ERROR] Error encountered while reading characteristic" + "\033[0m")


def get_client():
    try:
        adapter.start()
        device: GATTToolBLEDevice = adapter.connect(ADDRESS)
        print(f"Connected to device: {ADDRESS}")
        for handle, char in handles.items():
            print("0x%x: \"%s\"," % (handle, char), end=" ")
            value = read_characteristic(device, char)
            if value is not None:
                print("Value: ", value)

    finally:
        adapter.stop()


def read_register(register: hex) -> bytearray:
    try:
        adapter.start()
        device = adapter.connect(ADDRESS)
        handle = handles[register]
        value = read_characteristic(device, handle)
        print("Value: ", value)
        return value
    finally:
        adapter.stop()


def write_register(register: hex, val: bytearray, wait: bool = False):
    try:
        adapter.start()
        device = adapter.connect(ADDRESS)
        handle = handles[register]
        device.char_write(handle, val, wait_for_response=wait)
    finally:
        adapter.stop()


if __name__ == "__main__":
    get_client()


