# Random Number Generator (GUI Version)
import tkinter
from tkinter import messagebox
from random import *
import os
from datetime import datetime

GUI_COLOUR = "lavender"

rand_numbers = []  # final output

dt = datetime.now()
date_format = "%d/%m/%Y"
time_format = "%H:%M:%S"
text_file = os.path.expanduser("~/Desktop/random_numbers.txt")
with open(text_file, "a") as tf:  # Add today's date
    tf.write(f"\nNumbers generated on {dt.strftime(date_format)} at {dt.strftime(time_format)} \n\n")

# ------------------------- PASSWORD GENERATOR ---------------------------- #


def generate_numbers():
    clear_numbers()
    global rand_numbers
    try:
        gen = int(num_amount_box.get())
        low = int(low_num_box.get())
        high = int(high_num_box.get())
    except ValueError:
        messagebox.showinfo(title="Error", message="Please enter a number.")
    else:
        if unique_check() == 1:
            for number in range(0, gen):
                number = randint(low, high)
                while number in rand_numbers:
                    number = randint(low, high)
                rand_numbers.append(number)
        else:
            for i in range(0, gen):
                number = randint(low, high)
                rand_numbers.append(number)
    rand_numbers.sort()
    str_convert = (', '.join(map(str, rand_numbers)))  # Convert to a string so you can get rid of the square brackets
    output = final_numbers.config(text=f"{str_convert}")
    with open(text_file, "a") as data_file:  # Save to text file
        data_file.write(str_convert + "\n")
    output_label.config(text=f"File saved as {text_file}")
    return output


# ------------------------- CHECKBOX FOR UNIQUE --------------------------- #


def unique_check():
    # Prints 1 if checked, otherwise 0.
    return checked_state.get()

# ----------------------- CLEAR PREVIOUS NUMBERS -------------------------- #


def clear_numbers():
    global rand_numbers
    rand_numbers = []


# ----------------------------- GUI CONFIG -------------------------------- #

window = tkinter.Tk()
window.title("Random Number Generator")
window.minsize(width=400, height=200)
window.config(padx=20, pady=20, background=GUI_COLOUR)

# ----------------------------- LOGO IMAGE -------------------------------- #

canvas = tkinter.Canvas(width=524, height=78, bg=GUI_COLOUR, highlightthickness=0)
logo_img = tkinter.PhotoImage(file="logo.png")
canvas.create_image(262, 39, image=logo_img)
canvas.grid(column=0, row=0, columnspan=4, pady=10)

# ------------------------------- LABELS ---------------------------------- #
# Random Numbers Label
random_numbers_label = tkinter.Label(text="Your Numbers: ", font=("Arial", 12, "normal"))
random_numbers_label.config(padx=10, pady=10, borderwidth=1, background=GUI_COLOUR)
random_numbers_label.grid(row=1, column=0, sticky="w")

final_numbers = tkinter.Label(text=f"", font=("Arial", 18, "bold"))
final_numbers.config(padx=10, pady=10, borderwidth=1, background=GUI_COLOUR)
final_numbers.grid(row=1, column=1, columnspan=3, sticky="w")

# Numbers Required Label
num_amount_label = tkinter.Label(text="How many numbers?", font=("Arial", 12, "normal"))
num_amount_label.config(padx=10, pady=10, background=GUI_COLOUR)
num_amount_label.grid(column=0, row=2, sticky="w")

# Lowest Number Required Label
low_num_label = tkinter.Label(text="Low Number?", font=("Arial", 12, "normal"))
low_num_label.config(padx=10, pady=10, background=GUI_COLOUR)
low_num_label.grid(column=0, row=3, sticky="w")

# Highest Number Required Label
high_num_label = tkinter.Label(text="High Number?", font=("Arial", 12, "normal"))
high_num_label.config(padx=10, pady=10, background=GUI_COLOUR)
high_num_label.grid(column=2, row=3, sticky="w")

output_label = tkinter.Label(text=f"", font=("Arial", 10, "normal"))
output_label.config(padx=10, pady=10, background=GUI_COLOUR)
output_label.grid(column=0, row=5, columnspan=4, sticky="w")

# ------------------------------- CHECKBOX ---------------------------------- #
# Unique Numbers Tickbox
checked_state = tkinter.IntVar()
check_button = tkinter.Checkbutton(text="Unique?", variable=checked_state, command=unique_check)
check_button.config(background=GUI_COLOUR)
check_button.grid(column=2, row=2, sticky="e")
checked_state.get()

# ----------------------------- TEXT BOXES --------------------------------- #
# How Many Numbers Textbox
num_amount_box = tkinter.Entry(width=4)
num_amount_box.get()
num_amount_box.grid(column=1, row=2, sticky="w")

# Lowest Number Required Text box
low_num_box = tkinter.Entry(width=4)
low_num_box.get()
low_num_box.grid(column=1, row=3, sticky="w")

# Highest Number Required Text box
high_num_box = tkinter.Entry(width=4)
high_num_box.get()
high_num_box.grid(column=3, row=3, sticky="w")

# ------------------------------- BUTTON ---------------------------------- #
# Number Generator Button
button = tkinter.Button(text="Generate Numbers", command=generate_numbers)
button.grid(columnspan=4, row=4)
button.config(borderwidth=4, background=GUI_COLOUR, highlightbackground="black", activebackground="lightskyblue")

window.mainloop()
