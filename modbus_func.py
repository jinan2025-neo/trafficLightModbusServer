import time
from pymodbus.client.tcp import ModbusTcpClient

# Modbus server settings
MODBUS_SERVER_IP = '10.3.21.91'
MODBUS_SERVER_PORT = 502
UNIT_ID = 1

# Map: coil index to signal name
SIGNAL_MAP = {
    0: 'N_red', 1: 'N_orange', 2: 'N_green',
    3: 'EW_red', 4: 'EW_orange', 5: 'EW_green',
    6: 'S_red', 7: 'S_orange', 8: 'S_green'
}

# GUI Signal Light References
signal_widgets = {}

# Define layout for traffic lights
layout_order = ['N', 'EW', 'S']
colors = ['red', 'orange', 'green']

def read_signals(client):
    """
    Read 9 coil values from Modbus and return as dict.

    return in format:
    demo = [
        {"direction": "N", "address": 0, "coils": {"red": True,  "amber": False, "green": False}},
        {"direction": "EW", "address": 3, "coils": {"red": False, "amber": True,  "green": False}},
        {"direction": "S", "address": 6, "coils": {"red": False, "amber": False, "green": True}},
    ]
    """
    response = client.read_coils(address=0, count=9, device_id=UNIT_ID)
    if response.isError():
        print("Modbus read error.")
        return []
    signals = []
    for i in range(0, 9, 3):
        direction = layout_order[i // 3]
        address = i
        coils = {
            'red': response.bits[i],
            'amber': response.bits[i + 1],
            'green': response.bits[i + 2]
        }
        signals.append({"direction": direction, "address": address, "coils": coils})

    return signals
    # return {SIGNAL_MAP[i].split()[0]: result.bits[i], 'direction': SIGNAL_MAP[i].split()[1], 'address':i for i in range(9)}


if __name__ == "__main__":
    client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_SERVER_PORT)
    if not client.connect():
        print("Cannot connect to Modbus server.")
    else:
        try:
            while True:
                signals = read_signals(client)
                print(signals)  # For debugging
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopped by user.")
        finally:
            client.close()