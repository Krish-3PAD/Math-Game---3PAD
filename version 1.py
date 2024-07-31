from tkinter import*
from random import randint , choice

root = Tk()
root.geometry("500x500")
root.title("Math Quiz")

question = StringVar()
answer = StringVar()
givenAnswer = StringVar()

def generateQuestion():
    number1 = randint(1 , 10)
    number2 = randint(1 , 10)

    operator = choice(['+' , '-' , '*' , '/'])
    
    question.set(str(number1) + operator + str(number2))
    answer.set(eval(question.get())) 

    QuestionLabel = Label(root, text = question.get() ,  font = ("arial" , 20))
    QuestionLabel.grid( row = 1, column =0)
    

def checkAnswer():
    if str(answer.get()) == givenAnswer.get():
        resultLabel = Label(root, text ="Correct" , font = ('arial' , 20), fg = "green")
        resultLabel.grid(row = 3 , column = 0)
    else:
        resultLabel = Label(root, text ="Incorrect" , font = ('arial' , 20), fg = "red")
        resultLabel.grid(row = 3 , column = 0)

        generateQuestion()

generateQuestion()

   
# User Interface

headingLabel = Label(root, text= "Math Quiz", font = ("arial" , 20) )
headingLabel.grid(row=0 , column = 0)

questionLabel = Label(root , text = question.get() ,  font = ("arial" , 20))
questionLabel.grid( row = 1, column =0)

answerEntry = Entry(root, textvariable=givenAnswer , font= ('arial' , 20))
answerEntry.grid (row = 2 , column =0 )

submitButton = Button(root, text = "Submit" , font =("arial", 20), command= checkAnswer)
submitButton.grid(row = 2, column = 1)

root.mainloop()