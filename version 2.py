from tkinter import*
from random import randint , choice

root = Tk()
root.geometry("500x500")
root.title("Math Game")

question = StringVar()
answer = StringVar()
givenAnswer = StringVar()
score = IntVar()
questionNumber = IntVar()

def generateQuestion():

    global questionlabel

    questionNumber.set(questionNumber.get() + 1)

    number1 = randint(1, 10)
    number2 = randint(1, 10)

    operator = choice(['+' , '-' , '*' , '/'])

    question.set(str(number1) + operator + str(number2))
    answer.set(eval(question.get()))

    if questionLabel:
        questionLabel.destroy() 
    
    questionLabel = Label(root , text = f"Question : {question.get()}", font =("arial", 20))
    questionLabel.grid(row=2, column = 0)

    def checkAnswer ():

        global resultLabel

        if resultLabel:
            resultLabel.destroy()
        
        if str(answer.get() == givenAnswer.get()):
           score.set(score.get() + 1)
           resultLabel = Label(root , text = "Correct" , font = ("arial" , 20), fg = "green")
           resultLabel.grid(row = 4, column = 0)
           scoreLabel = Label(root , text =f"Score : {score.get()}", font=("arial" , 20), fg = "black")
           scoreLabel.grid(row = 5, column = 0)

        else:
           resultLabel = Label(root , text = "Correct" , font = ("arial" , 20), fg = "red")
           resultLabel.grid(row = 4, column = 0)

        generateQuestion()


        # User Interface 

        headingLabel = Label(root, text= "Math Game" , font = ("arial" , 20))
        headingLabel.grid (row= 0, column = 0)

        questionScale = Scale(root , from_=0, to=10, orient=HORIZONTAL, length=400, variable= questionNumber)
        questionScale.grid(row=1, column=0)

        completeQuestionLabel = Label(root, text="!0th Question")
        completeQuestionLabel.grid(row = 1, column= 1)

        questionLabel=Label(root, text=question.get(), font = ("arial", 20))
        questionLabel.grid(row= 2, column=0)

        answerEntry= Entry(root, textvariable= givenAnswer , font = ("arial" , 20))
        answerEntry.grid(row=3, column=1)

        submitButton = Button(root, text = "Submit" , font=("arial", 20) ,command= checkAnswer)
        submitButton.grid(row=3, column= 0)

        resultLabel = Label(root, text="Result", font =('arial' , 20), fg = "blue")
        resultLabel.grid(row=4, column=1)

        scoreLabel = Label(root, text=f"Score : {score.get()}" , font = ("arial" , 20) , fg ="black")
        scoreLabel.grid(row=5, column= 0)

        root.mainloop()


