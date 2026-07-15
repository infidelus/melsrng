#!/usr/bin/python3
# Random Number Generator with presets for Lotto and Euromillions

import tkinter
from tkinter import messagebox, ttk
from random import SystemRandom
import os
import sys
from datetime import datetime
import time


GUI_COLOUR = "lavender"
DELAY_DURATION = 60  # 1 minute delay

rand_numbers = []
text_file = ""
euromillions_mode = False


# ------------------------- NUMBER GENERATOR ---------------------------- #

def generate_numbers():
    global text_file, rand_numbers

    text_file = os.path.join(os.path.expanduser("~"), "Desktop", "random_numbers.txt")
    clear_numbers()

    date_format = "%d/%m/%Y"
    time_format = "%H:%M:%S"

    current_time = time.time()
    time_diff = current_time - generate_numbers.last_time if hasattr(generate_numbers, "last_time") else DELAY_DURATION + 1

    try:
        gen = int(num_amount_box.get())
        low = int(low_num_box.get())
        high = int(high_num_box.get())
    except ValueError:
        messagebox.showinfo(title="Error", message="Please enter valid numbers.")
        return

    rng = SystemRandom()

    if unique_check() == 1:
        while len(rand_numbers) < gen:
            number = rng.randint(low, high)
            if number not in rand_numbers:
                rand_numbers.append(number)
    else:
        for _ in range(gen):
            rand_numbers.append(rng.randint(low, high))

    rand_numbers.sort()

    lucky_stars = []
    if euromillions_mode:
        while len(lucky_stars) < 2:
            star = rng.randint(1, 12)
            if star not in lucky_stars:
                lucky_stars.append(star)
        lucky_stars.sort()

    main_numbers_text = ', '.join(map(str, rand_numbers))

    if euromillions_mode:
        stars_text = ', '.join(map(str, lucky_stars))
        display_text = f"{main_numbers_text}  |  ⭐ {stars_text}"
    else:
        display_text = main_numbers_text


    if time_diff >= DELAY_DURATION:
        with open(text_file, "a") as data_file:
            if data_file.tell() != 0:
                data_file.write("\n\n")
            data_file.write(
                f"Numbers generated on {datetime.now().strftime(date_format)} "
                f"at {datetime.now().strftime(time_format)}\n\n{display_text}"
            )
    else:
        with open(text_file, "a") as data_file:
            data_file.write(f"\n{display_text}")

    final_numbers.config(text=display_text)
    output_label.config(text=f"File saved as {text_file}")
    generate_numbers.last_time = current_time


# ------------------------- PRESET HANDLER ---------------------------- #

def preset_selected(event=None):
    global euromillions_mode

    preset = preset_var.get()

    num_amount_box.delete(0, tkinter.END)
    low_num_box.delete(0, tkinter.END)
    high_num_box.delete(0, tkinter.END)
    checked_state.set(0)
    euromillions_mode = False

    if preset == "Lotto":
        num_amount_box.insert(0, "6")
        low_num_box.insert(0, "1")
        high_num_box.insert(0, "59")
        checked_state.set(1)

    elif preset == "EuroMillions":
        num_amount_box.insert(0, "5")
        low_num_box.insert(0, "1")
        high_num_box.insert(0, "50")
        checked_state.set(1)
        euromillions_mode = True

    elif preset == "Manual":
        pass


# ------------------------- HELPERS ---------------------------- #

def unique_check():
    return checked_state.get()


def clear_numbers():
    global rand_numbers
    rand_numbers = []


# ----------------------------- GUI CONFIG -------------------------------- #

window = tkinter.Tk()
window.title("Random Number Generator")
window.minsize(width=420, height=260)
window.config(padx=20, pady=20, background=GUI_COLOUR)

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "TCombobox",
    fieldbackground=GUI_COLOUR,
    background=GUI_COLOUR,
    foreground="black"
)
style.map(
    "TCombobox",
    fieldbackground=[("readonly", GUI_COLOUR)],
    background=[("readonly", GUI_COLOUR)],
    foreground=[("readonly", "black")]
)


# ----------------------------- LOGO IMAGE -------------------------------- #

canvas = tkinter.Canvas(width=524, height=78, bg=GUI_COLOUR, highlightthickness=0)

# Resolve the absolute path to logo.png relative to this script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(script_dir, "logo.png")

logo_img = tkinter.PhotoImage(file=logo_path)
canvas.create_image(262, 39, image=logo_img)
canvas.grid(column=0, row=0, columnspan=4, pady=10)


# ----------------------------- PRESET DROPDOWN ---------------------------- #

preset_label = tkinter.Label(text="Preset:", font=("Arial", 12))
preset_label.config(padx=10, pady=10, background=GUI_COLOUR)
preset_label.grid(row=1, column=0, sticky="w")

preset_var = tkinter.StringVar(value="Manual")
preset_dropdown = ttk.Combobox(
    window,
    textvariable=preset_var,
    values=["Manual", "Lotto", "EuroMillions"],
    state="readonly",
    width=20
)
preset_dropdown.grid(row=1, column=1, columnspan=3, sticky="w")
preset_dropdown.bind("<<ComboboxSelected>>", preset_selected)


# ------------------------------- LABELS ---------------------------------- #

random_numbers_label = tkinter.Label(text="Your Numbers:", font=("Arial", 12))
random_numbers_label.config(padx=10, pady=10, background=GUI_COLOUR)
random_numbers_label.grid(row=2, column=0, sticky="w")

final_numbers = tkinter.Label(text="", font=("Arial", 16, "bold"), justify="left")
final_numbers.config(padx=10, pady=10, background=GUI_COLOUR)
final_numbers.grid(row=2, column=1, columnspan=3, sticky="w")

num_amount_label = tkinter.Label(text="How many numbers?", font=("Arial", 12))
num_amount_label.config(padx=10, pady=10, background=GUI_COLOUR)
num_amount_label.grid(column=0, row=3, sticky="w")

low_num_label = tkinter.Label(text="Low Number?", font=("Arial", 12))
low_num_label.config(padx=10, pady=10, background=GUI_COLOUR)
low_num_label.grid(column=0, row=4, sticky="w")

high_num_label = tkinter.Label(text="High Number?", font=("Arial", 12))
high_num_label.config(padx=10, pady=10, background=GUI_COLOUR)
high_num_label.grid(column=2, row=4, sticky="w")

output_label = tkinter.Label(text="", font=("Arial", 10))
output_label.config(padx=10, pady=10, background=GUI_COLOUR)
output_label.grid(column=0, row=6, columnspan=4, sticky="w")


# ------------------------------- CHECKBOX -------------------------------- #

checked_state = tkinter.IntVar()
check_button = tkinter.Checkbutton(text="Unique?", variable=checked_state)
check_button.config(background=GUI_COLOUR)
check_button.grid(column=2, row=3, sticky="e")


# ----------------------------- TEXT BOXES --------------------------------- #

num_amount_box = tkinter.Entry(width=4)
num_amount_box.grid(column=1, row=3, sticky="w")

low_num_box = tkinter.Entry(width=4)
low_num_box.grid(column=1, row=4, sticky="w")

high_num_box = tkinter.Entry(width=4)
high_num_box.grid(column=3, row=4, sticky="w")


# ------------------------------- BUTTON ---------------------------------- #

button = tkinter.Button(text="Generate Numbers", command=generate_numbers)
button.grid(columnspan=4, row=5)
button.config(
    borderwidth=4,
    background=GUI_COLOUR,
    highlightbackground="black",
    activebackground="lightskyblue"
)

window.mainloop()
