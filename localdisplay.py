import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import yaml

def fetch_network_info():
    # Parsing netplan's yaml configuration
    with open("/etc/netplan/01-network-manager-all.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    try:
        ip_info = config['network']['ethernets']['eth0']['addresses'][0]
        ip = ip_info.split('/')[0]  # Splitting CIDR notation to get just the IP
        return ip
    except:
        return "Not found"

def set_network_info(ip):
    config = {
        'network': {
            'version': 2,
            'renderer': 'networkd',
            'ethernets': {
                'eth0': {
                    'dhcp4': False,
                    'addresses': [f'{ip}/24']
                }
            }
        }
    }
    with open("/etc/netplan/01-network-manager-all.yaml", "w") as f:
        yaml.dump(config, f)
    
    os.system("sudo netplan apply")

def apply_changes():
    ip = ip_entry.get()
    
    # You can add more validation here
    if not ip:
        messagebox.showerror("Error", "Please enter a valid IP address.")
        return
    
    set_network_info(ip)
    messagebox.showinfo("Success", "Network settings updated. Restart may be needed.")

app = tk.Tk()
app.title("Ubuntu Network Config")

frame = tk.Frame(app)
frame.pack(padx=20, pady=20)

tk.Label(frame, text="IP Address").grid(row=0, column=0, padx=10, pady=10, sticky="e")
ip_entry = tk.Entry(frame)
ip_entry.grid(row=0, column=1, padx=10, pady=10)
ip_entry.insert(0, fetch_network_info())

btn_apply = tk.Button(frame, text="Apply", command=apply_changes)
btn_apply.grid(row=1, column=0, columnspan=2, pady=20)

app.mainloop()
