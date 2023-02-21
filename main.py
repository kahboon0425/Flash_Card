from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    # TODO : remove the word the user know
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill = "black")
    canvas.itemconfig(card_word, text=current_card["French"], fill = "black")
    canvas.itemconfig(card_background, image=card_front)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image = card_back)

def is_known():
    # current_card is a dictionary which we chosen randomly from the list of dictionary
    to_learn.remove(current_card)
    print(len(to_learn))

    # store the data that still need to learn
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index = False)
    next_card()

window = Tk()
window.title("Flash Card")
# window.minsize(width=800, height=750)
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front = PhotoImage(file = "images/card_front.png")
card_back = PhotoImage(file = "images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400,263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

wrong_icon = PhotoImage(file = "images/wrong.png")
canvas_wrong = Button(image=wrong_icon, highlightthickness=0, command=next_card)
canvas_wrong.grid(column=1, row=1)

correct_icon = PhotoImage(file = "images/right.png")
canvas_correct = Button(image=correct_icon, highlightthickness=0, command=is_known)
canvas_correct.grid(column=0, row=1)


next_card()

window.mainloop()
