from tkinter import *
from tkinter import messagebox
from random import randint, choice
import time

class MathQuiz:
    def __init__(self):
        self.score = 0
        self.question_number = 0
        self.start_time = 0
        self.current_answer = None

    def generate_question(self):
        number1 = randint(1, 10)
        number2 = randint(1, 10)
        operator = choice(['+', '-', '*', '/'])

        # Ensure division does not result in non-integer answers
        if operator == '/':
            if number2 == 0:
                number2 = 1  # Prevent division by zero
            # Ensure that number1 is divisible by number2
            number1 = number2 * randint(1, 10)
        
        # Compute the answer based on the operator
        if operator == '+':
            self.current_answer = number1 + number2
        elif operator == '-':
            self.current_answer = number1 - number2
        elif operator == '*':
            self.current_answer = number1 * number2
        elif operator == '/':
            self.current_answer = number1 // number2  # Use integer division
        
        question = f"{number1} {operator} {number2}"
        return question

    def check_answer(self, user_answer):
        return str(self.current_answer) == str(user_answer)

    def increment_score(self):
        self.score += 1

    def reset(self):
        self.score = 0
        self.question_number = 0

class MathQuizApp:
    TIME_LIMIT = 8  # Time limit in seconds

    def __init__(self, root):
        self.root = root
        self.root.geometry("450x700")  # Increased window size
        self.root.title("Maths Quiz")
        self.root.configure(bg='black')  # Set background color to black

        self.quiz = MathQuiz()

        # UI Elements
        self.question = StringVar()
        self.answer = StringVar()
        self.given_answer = StringVar()
        
        self.create_widgets()
        self.generate_question()

    def create_widgets(self):
        # Top section
        self.heading_label = Label(self.root, text="Maths Quiz", font=('Arial', 30), fg="#73e5ff", bg='black')
        self.heading_label.grid(row=0, column=0, columnspan=2, pady=(20, 20))

        # Frame for question and score
        self.top_frame = Frame(self.root, bg='black')
        self.top_frame.grid(row=1, column=0, columnspan=2, pady=(10, 20), sticky="w")

        self.question_number_label = Label(self.top_frame, text=f"{self.quiz.question_number})", font=('arial', 20), fg="#73e5ff", bg='black')
        self.question_number_label.grid(row=0, column=0, padx=(10, 5), sticky="w")

        self.question_label = Label(self.top_frame, text="", font=('calibri', 20), bg='black', fg='#73e5ff')
        self.question_label.grid(row=0, column=1, padx=(10, 5), sticky="w")

        self.score_label = Label(self.top_frame, text=f"Score : {self.quiz.score}", font=('arial', 20), fg="#73e5ff", bg='black')
        self.score_label.grid(row=0, column=2, padx=(10, 5), sticky="w")

        self.timer_label = Label(self.root, text="", font=('arial', 20), fg="#73e5ff", bg='black')
        self.timer_label.grid(row=2, column=0, columnspan=2, pady=(15, 100))  # Increased bottom padding for larger gap

        # Frame for entry and submit button
        self.entry_frame = Frame(self.root, bg='black')
        self.entry_frame.grid(row=3, column=0, columnspan=2, pady=(10, 5), sticky="w")

        self.answer_entry = Entry(self.entry_frame, textvariable=self.given_answer, font=('arial', 20), width=20)
        self.answer_entry.grid(row=0, column=0, padx=(10, 5))

        self.submit_button = Button(self.entry_frame, text="Submit", fg="#73e5ff", bg="#000000", font=('arial', 15), command=self.check_answer)
        self.submit_button.grid(row=0, column=1, padx=(5, 10))

        # Restart button below entry box
        self.restart_button = Button(self.root, text="Restart", fg="red", font=('arial', 15), width=35, command=self.restart, bg='black', activebackground='black', activeforeground='red')
        self.restart_button.grid(row=4, column=0, columnspan=2, pady=(10, 20))

        # Result label
        self.result_label = Label(self.root, text="", font=('arial', 20), bg='black')
        self.result_label.grid(row=5, column=0, columnspan=2, pady=(10, 20))

        self.answer_entry.bind('<Return>', self.check_answer)

    def generate_question(self):
        self.quiz.question_number += 1
        question_text = self.quiz.generate_question()
        self.question.set(question_text)
        self.answer.set(self.quiz.current_answer)

        self.question_label.config(text=f"Question : {self.question.get()}")
        self.start_time = time.time()  # Record start time for countdown

        self.countdown()

        self.given_answer.set('')
        self.question_number_label.config(text=f"{self.quiz.question_number})")

    def countdown(self):
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = self.TIME_LIMIT - elapsed_time

        if remaining_time <= 0:
            self.result_label.config(text="Time's up!", fg="red")
            self.generate_question()  # Proceed to next question
        else:
            self.timer_label.config(text=f"Time left: {remaining_time} seconds")
            self.root.after(1000, self.countdown)  # Update every second

    def check_answer(self, event=None):
        if self.quiz.question_number >= 10:
            if messagebox.askyesno("Game Over", f"Game Over! Your final score is {self.quiz.score}. Do you want to play again?"):
                self.restart()  # Restart the game if user chooses to play again
            else:
                self.root.quit()  # Exit the application if user chooses not to play again
            return

        try:
            user_answer = int(self.given_answer.get())  # Attempt to convert input to integer
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")
            return

        if self.quiz.check_answer(user_answer):
            self.quiz.increment_score()
            self.result_label.config(text="Correct", font=('arial', 20), fg="#76F984", bg='black')
        else:
            self.result_label.config(text="Incorrect", font=('arial', 20), fg="red", bg='black')

        self.score_label.config(text=f"Score : {self.quiz.score}")

        if self.quiz.question_number >= 10:
            self.score_label.config(text=f"Final Score : {self.quiz.score}")
            self.submit_button.config(state=DISABLED)
        else:
            self.generate_question()

        self.given_answer.set('')

    def restart(self):
        self.quiz.reset()
        self.generate_question()
        self.score_label.config(text=f"Score : {self.quiz.score}")
        self.submit_button.config(state=NORMAL)
        self.question_number_label.config(text=f"{self.quiz.question_number})")

if __name__ == "__main__":
    root = Tk()
    app = MathQuizApp(root)
    root.mainloop()
