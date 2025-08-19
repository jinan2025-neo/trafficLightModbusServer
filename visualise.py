import time
import tkinter as tk
from pymodbus.client.tcp import ModbusTcpClient
from threading import Thread

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
    """
    result = client.read_coils(address=0, count=9, slave=UNIT_ID)
    if result.isError():
        print("Modbus read error.")
        return {}
    return {SIGNAL_MAP[i]: result.bits[i] for i in range(9)}

def update_gui_signals(signal_states):
    """
    Update each light circle based on Modbus state.
    """
    for name, state in signal_states.items():
        widget = signal_widgets.get(name)
        if widget:
            color = name.split('_')[1]  # red, orange, green
            widget.config(bg=color if state else "gray20")

def polling_loop():
    client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_SERVER_PORT)
    if not client.connect():
        print("Cannot connect to Modbus server.")
        return

    while True:
        signal_states = read_signals(client)
        if signal_states:
            update_gui_signals(signal_states)
        time.sleep(1)

def create_gui():
    window = tk.Tk()
    window.title("Traffic Light Monitor")
    window.configure(bg='black')

    for row, direction in enumerate(layout_order):
        tk.Label(window, text=direction, fg="white", bg="black", font=('Arial', 14)).grid(row=row, column=0, padx=10)
        for col, color in enumerate(colors):
            name = f"{direction}_{'orange' if color == 'orange' else color}"
            lbl = tk.Label(window, bg="gray20", width=8, height=3, relief="ridge")
            lbl.grid(row=row, column=col+1, padx=5, pady=5)
            signal_widgets[name] = lbl

    # Start Modbus polling in a separate thread
    Thread(target=polling_loop, daemon=True).start()
    window.mainloop()

if __name__ == "__main__":
    create_gui()
