BACKGROUND_COLOR = "#B1DDC6"

from tkinter import *
import pandas as pd
import random
import pandas.io.common

curr_card = {}
known_words= {}

try:
    learning = pd.read_csv("data/french.csv").to_dict(orient="records")
except FileNotFoundError:
    learning = pd.read_csv("data/french_words.csv").to_dict(orient="records")
except pd.errors.EmptyDataError:
    learning = [{'French': 'Course Completed', 'English': 'Course Completed'}]

def known():
    if (learning[0]['French'] != 'Course Completed'):
        learning.remove(curr_card)
        new_list = pd.DataFrame(learning)
        new_list.to_csv("data/french.csv", index=False)

def next(pressed):
    if len(learning) == 0:
        canvas.itemconfig(title_card, text="Learning Completed")
        canvas.itemconfig(word_card, text="")
    global curr_card, flip_timer
    window.after_cancel(flip_timer)
    try:
        curr_card = random.choice(learning)
    except IndexError:
        curr_card = {'French': 'Course Completed', 'English': 'Course Completed'}
    value = curr_card["French"]
    canvas.itemconfig(title_card, text="French", fill="black")
    canvas.itemconfig(word_card, text=value, fill="black")
    canvas.itemconfig(card_bg, image=bgImg)
    if pressed == "Known":
        known()
    flip_timer = window.after(3000, func=flipCard)


def flipCard():
    canvas.itemconfig(title_card, text="English", fill="white")
    value = curr_card["English"]
    canvas.itemconfig(word_card, text=value, fill="white")
    canvas.itemconfig(card_bg, image=flipImg)


window = Tk()
window.title("Flash Quiz")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
bgImg = PhotoImage(file="images/card_front.png")
flipImg = PhotoImage(file="images/card_back.png")

flip_timer = window.after(3000, func=flipCard)

canvas = Canvas(width=800, height=526)
card_bg = canvas.create_image(400, 263, image=bgImg)
title_card = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word_card = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

#button
rightImg = PhotoImage(file="images/right.png")
wrongImg = PhotoImage(file="images/wrong.png")
right = Button(image=rightImg, command=lambda m="Known":next(m))
right.grid(row=1, column=0)
wrong = Button(image=wrongImg, command=lambda m="Unknown":next(m))
wrong.grid(row=1, column=1)

next("First_Time")

window.mainloop()



