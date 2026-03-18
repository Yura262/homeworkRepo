import os
import tkinter as tk
from tkinter import messagebox

search_paths = [
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\Python"),
    os.path.expandvars(r"%ProgramFiles%\Python"),
    os.path.expandvars(r"%ProgramFiles(x86)%\Python"),
    r"C:\Python",
]

def find_pythons():
    found = []

    for base in search_paths:
        if os.path.exists(base):
            for root, dirs, files in os.walk(base):
                if "python.exe" in files:
                    found.append(root)

    return sorted(set(found))

def add_to_path(path):
    user_path = os.environ.get("PATH", "")
    scripts = os.path.join(path, "Scripts")

    new_entries = []

    if path not in user_path:
        new_entries.append(path)

    if os.path.exists(scripts) and scripts not in user_path:
        new_entries.append(scripts)

    if not new_entries:
        messagebox.showinfo("Info", "Python is already in PATH")
        return

    new_path = user_path + ";" + ";".join(new_entries)

    os.system(f'setx PATH "{new_path}"')

    messagebox.showinfo(
        "Success",
        f"Added to PATH:\n\n" + "\n".join(new_entries) +
        "\n\nRestart terminal for changes to apply."
    )

def install():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Warning", "Select a Python installation first")
        return

    path = python_paths[selection[0]]
    add_to_path(path)

python_paths = find_pythons()

root = tk.Tk()
root.title("Python PATH Fixer")
root.geometry("500x350")

label = tk.Label(root, text="Detected Python installations:")
label.pack(pady=10)

listbox = tk.Listbox(root, width=70, height=10)
listbox.pack()

for p in python_paths:
    listbox.insert(tk.END, p)

if not python_paths:
    listbox.insert(tk.END, "No Python installations found")

btn = tk.Button(root, text="Add Selected Python to PATH", command=install)
btn.pack(pady=20)

root.mainloop()