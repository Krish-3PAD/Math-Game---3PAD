from tkinter import *
from random import randint, choice

root = Tk()
root.geometry("488x500")
root.title("Maths Quiz")
root.configure(bg='black')  # Set root window background color to black

question = StringVar()
answer = StringVar()
givenAnswer = StringVar()
score = IntVar()
questionNumber = IntVar()

def generateQuestion():
    global questionLabel

    questionNumber.set(questionNumber.get() + 1)

    number1 = randint(1, 10)
    number2 = randint(1, 10)

    operator = choice(['+', '-', '*', '/'])

    question.set(str(number1) + operator + str(number2))
    answer.set(eval(question.get()))

    if questionLabel:
        questionLabel.destroy()

    questionLabel = Label(root, text=f"Question : {question.get()}", font=('arial', 20), bg='black', fg='#7CE5FF')  # Set background and foreground color for Label
    questionLabel.grid(row=2, column=0)

def checkAnswer():
    global scoreLabel

    if questionNumber.get() > 10:
        return

    global resultLabel

    if resultLabel:
        resultLabel.destroy()

    if str(answer.get()) == givenAnswer.get():
        score.set(score.get() + 1)
        resultLabel = Label(root, text="Correct", font=('arial', 20), fg="#76F984", bg='black')  # Set background color for Label
        resultLabel.grid(row=4, column=0)
        scoreLabel = Label(root, text=f"Score : {score.get()}", font=('arial', 20), fg="#7CE5FF", bg='black')  # Set background and foreground color for Label
        scoreLabel.grid(row=5, column=0)

    else:
        resultLabel = Label(root, text="Incorrect", font=('arial', 20), fg="red", bg='black')  # Set background color for Label
        resultLabel.grid(row=4, column=0)

    if questionNumber.get() == 10:
        scoreLabel.destroy()
        scoreLabel = Label(root, text=f"Final Score : {score.get()}", font=('arial', 20), fg="#7CE5FF", bg='black')  # Set background and foreground color for Label
        scoreLabel.grid(row=5, column=0)
    else:
        generateQuestion()

def restart():
    global scoreLabel
    scoreLabel.destroy()

    score.set(0)
    questionNumber.set(0)
    generateQuestion()

    scoreLabel = Label(root, text=f"Score : {score.get()}", font=('arial', 20), fg="#7CE5FF", bg='black')  # Set background and foreground color for Label
    scoreLabel.grid(row=5, column=0)

# User Interface

headingLabel = Label(root, text="Maths Quiz", font=('arial', 30), fg="#7CE5FF", bg='black')  # Set background and foreground color for Label
headingLabel.grid(row=0, column=0)

questionLabel = Label(root, text=question.get(), font=('calibri', 20), bg='#7CE5FF', fg='#7CE5FF')  # Set background and foreground color for Label
questionLabel.grid(row=2, column=0)

answerEntry = Entry(root, textvariable=givenAnswer, font=('arial', 20), width=25)
answerEntry.grid(row=3, column=0)

submitButton = Button(root, text="Submit", fg="#7CE5FF", bg="#000000", font=('arial', 15), command=checkAnswer)
submitButton.grid(row=3, column=1)

resultLabel = Label(root, text="Result", font=('arial', 20), fg="#7CE5FF", bg='black')  # Set background color for Label
resultLabel.grid(row=4, column=0)

scoreLabel = Label(root, text=f"Score : {score.get()}", font=('arial', 20), fg="#7CE5FF", bg='black')  # Set background and foreground color for Label
scoreLabel.grid(row=5, column=0)

restartButton = Button(root, text="Restart", fg="red", font=('arial', 15), width=35, command=restart, bg='black', activebackground='black', activeforeground='red')  # Set background and foreground color for Button
restartButton.grid(row=6, column=0)

generateQuestion()

root.mainloop()
