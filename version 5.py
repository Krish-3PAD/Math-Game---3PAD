from tkinter import *
from tkinter import messagebox
from random import randint, choice
import time

root = Tk()
root.geometry("488x500")
root.title("Maths Quiz")
root.configure(bg='black')  # Set root window background color to black

question = StringVar()
answer = StringVar()
givenAnswer = StringVar()
score = IntVar()
questionNumber = IntVar()

TIME_LIMIT = 8  # Time limit in seconds

def generateQuestion():
    global questionLabel, start_time

    questionNumber.set(questionNumber.get() + 1)

    number1 = randint(1, 10)
    number2 = randint(1, 10)

    operator = choice(['+', '-', '*', '/'])

    # Ensure division does not result in non-integer answers
    if operator == '/' and number1 % number2 != 0:
        number1 = number2 * randint(1, 10)  # Ensure a valid division

    question.set(f"{number1} {operator} {number2}")
    if operator == '/':
        answer.set(int(number1 / number2))
    else:
        answer.set(eval(question.get()))

    if questionLabel:
        questionLabel.destroy()

    questionLabel = Label(root, text=f"Question : {question.get()}", font=('arial', 20), bg='black', fg='#D280F3')  # Set background and foreground color for Label
    questionLabel.grid(row=2, column=0)

    start_time = time.time()  # Record start time for countdown

    # Start countdown timer
    countdown()

def countdown():
    global start_time

    elapsed_time = int(time.time() - start_time)
    remaining_time = TIME_LIMIT - elapsed_time

    if remaining_time <= 0:
        # Time's up, mark as incorrect
        resultLabel = Label(root, text="", font=('arial', 20), fg="red", bg='white')
        resultLabel.grid(row=4, column=0)
        generateQuestion()  # Proceed to next question
    else:
        # Update timer display
        timerLabel.config(text=f"Time left: {remaining_time} seconds")
        root.after(1000, countdown)  # Update every second

def checkAnswer():
    global scoreLabel

    if questionNumber.get() > 10:
        return

    global resultLabel

    if resultLabel:
        resultLabel.destroy()

    try:
        user_answer = int(givenAnswer.get())  # Attempt to convert input to integer
    except ValueError:
        messagebox.showerror("Error", "Please enter an integer")
        return

    if str(answer.get()) == str(user_answer):
        score.set(score.get() + 1)
        resultLabel = Label(root, text="Correct", font=('arial', 20), fg="#76F984", bg='black')
        resultLabel.grid(row=5, column=0)
        scoreLabel.config(text=f"Score : {score.get()}")  # Update score label
    else:
        resultLabel = Label(root, text="Incorrect", font=('arial', 20), fg="red", bg='black')
        resultLabel.grid(row=5, column=0)

    if questionNumber.get() == 10:
        scoreLabel.destroy()
        scoreLabel = Label(root, text=f"Final Score : {score.get()}", font=('arial', 20), fg="#D280F3", bg='black')
        scoreLabel.grid(row=5, column=0)
    else:
        generateQuestion()

def restart():
    global scoreLabel

    scoreLabel.destroy()

    score.set(0)
    questionNumber.set(0)
    generateQuestion()

    scoreLabel = Label(root, text=f"Score : {score.get()}", font=('arial', 20), fg="#D280F3", bg='black')  # Set background and foreground color for Label
    scoreLabel.grid(row=5, column=0)

# User Interface

headingLabel = Label(root, text="Maths Quiz", font=('arial', 30), fg="#D280F3", bg='black')  # Set background and foreground color for Label
headingLabel.grid(row=0, column=0)

questionLabel = Label(root, text="", font=('calibri', 20), bg='#D280F3', fg='#D280F3')  # Set background and foreground color for Label
questionLabel.grid(row=2, column=0)

timerLabel = Label(root, text="", font=('arial', 20), fg="#D280F3", bg='black')
timerLabel.grid(row=3, column=0)

answerEntry = Entry(root, textvariable=givenAnswer, font=('arial', 20), width=25)
answerEntry.grid(row=4, column=0)

submitButton = Button(root, text="Submit", fg="#D280F3", bg="#000000", font=('arial', 15), command=checkAnswer)
submitButton.grid(row=4, column=1)

resultLabel = Label(root, text="Result", font=('arial', 20), fg="#D280F3", bg='black')  # Set background color for Label
resultLabel.grid(row=5, column=0)

scoreLabel = Label(root, text=f"Score : {score.get()}", font=('arial', 20), fg="#D280F3", bg='black')  # Set background and foreground color for Label
scoreLabel.grid(row=6, column=0)

restartButton = Button(root, text="Restart", fg="red", font=('arial', 15), width=35, command=restart, bg='black', activebackground='black', activeforeground='red')  # Set background and foreground color for Button
restartButton.grid(row=7, column=0)

generateQuestion()

root.mainloop()
