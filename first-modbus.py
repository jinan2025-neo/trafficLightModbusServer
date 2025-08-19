from pymodbus.client.tcp import ModbusTcpClient

client = ModbusTcpClient('10.3.21.91', port=502)
client.connect()

# Read 9 coils (from %QX0.0 to %QX1.0 = coil address 0 to 8)
response = client.read_coils(address=0, count=9, unit=1)  # unit=1 is the default slave ID

# Check response
if response.isError():
    print("Error reading coils:", response)
else:
    # Print each coil value
    for i, coil in enumerate(response.bits):
        print(f"QX{i // 8}.{i % 8} = {coil}")

# Close connection
client.close()