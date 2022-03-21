from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
# Not a constant, but need a global variable to keep track of total reps done
# during session
reps = 0
# Not a constant, but used later to start and stop the window.after methods
timer = None


# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global timer
    window.after_cancel(timer)
    header_label.config(text="Timer", fg=GREEN)
    checkmark.config(text="")
    canvas.itemconfig(timer_text, text="25:00")
    global reps
    reps = 0
    start_button.config(state="active")
    reset_button.config(state="disabled")


# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    # Increment global reps variable
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # If the rep is the 8th rep, have a long break
    if reps % 8 == 0:
        countdown(long_break_sec)
        header_label.config(text="Break!", fg=RED)
    # If it is an even rep (aka, divisible by 2), have a short break
    elif reps % 2 == 0:
        countdown(short_break_sec)
        header_label.config(text="Break!", fg=PINK)
    # Any rep not a break rep is a working rep
    else:
        countdown(work_sec)
        header_label.config(text="Work!", fg=GREEN)
    start_button.config(state="disabled")
    reset_button.config(state="active")


# -------------------------- COUNTDOWN MECHANISM ----------------------------- #
def countdown(count):
    count_in_min = count // 60
    count_in_sec = count % 60
    canvas.itemconfig(timer_text, text=f"{count_in_min:02}:{count_in_sec:02}")
    if count > 0:
        global timer
        timer = window.after(1000, countdown, count - 1)
    # Once count goes to 0
    else:
        window.state("normal")
        window.attributes("-topmost", 1)
        window.attributes("-topmost", 0)
        start_timer()
        marks = ""
        for _ in range(reps//2):
            marks += "✔"
        checkmark.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
# Initialize Tk object and set up window
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=100, bg=YELLOW)

# PhotoImage object for the image to display in canvas and program icon
tomato_img = PhotoImage(file="tomato.png")

# Change icon using PhotoImage object
window.iconphoto(False, tomato_img)

# Create label for header
header_label = Label(text="Timer", font=(FONT_NAME, 40, "bold"), fg=GREEN, bg=YELLOW)
header_label.grid(column=1, row=0)

# Set up canvas to overlay objects on top of each other
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
# Display image from PhotoImage object
canvas.create_image(100, 112, image=tomato_img)
# Display timer text
timer_text = canvas.create_text(
    100, 130, text="25:00", fill="white", font=(FONT_NAME, 35, "bold")
)
# Actualize widgets with pack display method
canvas.grid(column=1, row=1)

# Start button
start_button = Button(text="Start", command=start_timer, highlightthickness=0)
start_button.grid(column=0, row=2)

# Reset button
reset_button = Button(text="Reset", command=reset_timer, highlightthickness=0)
reset_button.config(state="disabled")
reset_button.grid(column=2, row=2)

# Checkmark Label
checkmark = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 18, "bold"))
checkmark.grid(column=1, row=3)

# Mainloop to display window, must be last line of code
window.mainloop()
