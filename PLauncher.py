import tkinter as tk
from tkinter import PhotoImage, Toplevel
import subprocess

def change_background_color(color):
    window.configure(bg=color)

def open_world_creator():
    world_creator_window = Toplevel(window)
    world_creator_window.title("World List")
    world_creator_window.geometry('600x250')

    w1_button = tk.Button(world_creator_window, text="World 1", command=open_world_1)
    w1_button.pack(pady=10)

    w2_button = tk.Button(world_creator_window, text="World 2", command=open_world_2)
    w2_button.pack(pady=10)

    w3_button = tk.Button(world_creator_window, text="World 3", command=open_world_3)
    w3_button.pack(pady=10)

def open_world_1():
    try:
        subprocess.run(["python", "w1.py"])
    except Exception as e:
        print(f"Error running the script: {e}")

def open_world_2():
    try:
        subprocess.run(["python", "w2.py"])
    except Exception as e:
        print(f"Error running the script: {e}")

def open_world_3():
    try:
        subprocess.run(["python", "w3.py"])
    except Exception as e:
        print(f"Error running the script: {e}")

def open_options():
    world_creator_window = Toplevel(window)
    world_creator_window.title("Options")
    world_creator_window.geometry('600x250')

    w1_button = tk.Button(world_creator_window, text="Null")
    w1_button.pack(pady=10)

    w2_button = tk.Button(world_creator_window, text="Null")
    w2_button.pack(pady=10)

    w3_button = tk.Button(world_creator_window, text="Null")
    w3_button.pack(pady=10)

# Ana pencere
window = tk.Tk()
window.title("PLauncher")
window.geometry('600x300')

# Logo
logo_path = "MasterCraft.png"
logo_image = PhotoImage(file=logo_path)
label_logo = tk.Label(window, image=logo_image)
label_logo.pack(pady=10)

# "Singleplayer" tuşu
button_run_script = tk.Button(window, text="Singleplayer", command=open_world_creator)
button_run_script.pack(pady=10)

button_run_script = tk.Button(window, text="Options", command=open_options)
button_run_script.pack(pady=10)

# "Quit" tuşu
button_quit = tk.Button(window, text="Quit Game", command=window.quit)
button_quit.pack(pady=10)

# Ana döngü
window.mainloop()
