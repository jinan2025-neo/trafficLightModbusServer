import time
from pymodbus.client.tcp import ModbusTcpClient

MODBUS_SERVER_IP = '10.3.243.70'
MODBUS_SERVER_PORT = 502

def on_off_coil(client, value):
    # value: True(on) or False(off)
    # this will write the value into coil 801 (Run_AM), once write to false, the traffic light will be truned off
    result = client.write_coil(801, value)
    if result.isError():
        print('failed to write to coil 801(Run_AM)')
        return False
    else:
        print('successed to write to coil 801(Run_AM)')
        return True


if __name__ == "__main__":
    client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_SERVER_PORT)
    if not client.connect():
        print("Cannot connect to Modbus server.")
    else:
        try:
            on_off_coil(client, False)  # Turn off the traffic light system
        except KeyboardInterrupt:
            print("\nStopped by user.")
        finally:
            client.close()