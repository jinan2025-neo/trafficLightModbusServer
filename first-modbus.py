from pymodbus.client.tcp import ModbusTcpClient
import time

# --- Configuration ---
MODBUS_SERVER_IP = '10.3.21.91'
MODBUS_SERVER_PORT = 502
# Read 9 coils (from %QX0.0 to %QX1.0 = coil address 0 to 8)
# slave=1 is the default slave ID
COIL_ADDRESS = 0  # Address of the coil to read (0-based)
UNIT_ID = 1       # Usually 1 for Modbus TCP
INTERVAL = 1      # Time interval in seconds
def read_each_LEDs(client, time_interval=INTERVAL):
    response = client.read_coils(address=COIL_ADDRESS, count=9, device_id=UNIT_ID)
    if response.isError():
        print("Error reading coil.")
    else:
        # Print each coil value
        for i, coil in enumerate(response.bits):
            print(f"QX{i // 8}.{i % 8} = {coil}")
            if i>8:
                print('====================')
                break
    time.sleep(time_interval)
def main():
    client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_SERVER_PORT)
    connection = client.connect()

    if not connection:
        print("Unable to connect to Modbus server.")
        return

    try:
        # == write and change the mode_flag ==
        result = client.write_coil(800, False)

        if result.isError():
            print('failed to write to coil 800')
        else:
            print('successed')

        # == read every coils and update each INTERVAL sec
        # while True:
        #     read_each_LEDs(client)

    except KeyboardInterrupt:
        print("\nStopped by user.")

    finally:
        client.close()

if __name__ == "__main__":
    main()
