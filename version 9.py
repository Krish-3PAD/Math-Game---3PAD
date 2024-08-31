import json
from tkinter import *
from tkinter import messagebox
from random import randint, choice
import time

class MathQuiz:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.score = 0
        self.question_number = 0
        self.start_time = 0
        self.current_answer = None
        self.set_difficulty()

    def set_difficulty(self):
        if self.difficulty == 'Easy':
            self.num_range = (1, 10)
            self.operations = ['+','-',' *']
            self.hitpoints_decrement = 10
        elif self.difficulty == 'Medium':
            self.num_range = (7, 15)
            self.operations = ['+', '-', '*', "/"]
            self.hitpoints_decrement = 15
        else:  # Hard
            self.num_range = (12, 18)
            self.operations = ['+', '-', '*', '/']
            self.hitpoints_decrement = 15

    def generate_question(self):
        number1 = randint(*self.num_range)
        number2 = randint(*self.num_range)
        operator = choice(self.operations)

        # Ensure division does not result in non-integer answers
        if operator == '/':
            if number2 == 0:
                number2 = 1
            number1 = number2 * randint(1, 10)  # Make sure the result is an integer

        # Compute the answer based on the operator
        if operator == '+':
            self.current_answer = number1 + number2
        elif operator == '-':
            self.current_answer = number1 - number2
        elif operator == '*':
            self.current_answer = number1 * number2
        elif operator == '/':
            self.current_answer = number1 // number2

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
    Question_Timer = 4  # Time limit for each question in seconds.

    def __init__(self, root, difficulty):
        self.root = root
        self.root.geometry("820x1000")
        self.root.title("Maths Quiz")
        self.root.configure(bg='black')

        self.quiz = MathQuiz(difficulty)
        self.difficulty = difficulty

        # Initialize hitpoints
        self.player_hitpoints = 100
        self.enemy_hitpoints = 100

        # UI Elements
        self.question = StringVar()
        self.answer = StringVar()
        self.given_answer = StringVar()

        self.Widjets()
        self.generate_question()

    def Widjets(self):
        self.title_label = Label(self.root, text="Maths Quiz", font=('Times', 29), fg="#73e5ff", bg='black')
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(20, 20))

        self.top_frame = Frame(self.root, bg='black')
        self.top_frame.grid(row=1, column=0, columnspan=3, pady=(10, 20), sticky="ew")

        self.question_number_label = Label(self.top_frame, text=f"{self.quiz.question_number})", font=('Times', 19), fg="#73e5ff", bg='black')
        self.question_number_label.grid(row=0, column=0, padx=(10, 5), sticky="e")

        self.question_label = Label(self.top_frame, text="", font=('calibri', 19), bg='#73e5ff', fg='black')
        self.question_label.grid(row=0, column=1, padx=(15, 5), sticky="nsew")

        self.score_label = Label(self.top_frame, text=f"Score : {self.quiz.score}", font=('Times', 19), fg="#73e5ff", bg='black')
        self.score_label.grid(row=0, column=2, padx=(10, 5), sticky="w")

        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=1)
        self.top_frame.grid_columnconfigure(2, weight=1)

        self.timer_label = Label(self.root, text="", font=('Times', 19), fg="#73e5ff", bg='black')
        self.timer_label.grid(row=2, column=0, columnspan=3, pady=(15, 20))

        self.canvas = Canvas(self.root, width=815, height=535, bg='purple')
        self.canvas.grid(row=3, column=0, columnspan=3, pady=(10, 20))

        self.background_image = PhotoImage(file="background.png")
        self.background = self.canvas.create_image(400, 300, image=self.background_image, anchor=CENTER)

        self.player_idle_image = PhotoImage(file="player_idle.png") 
        self.player_strike_image = PhotoImage(file="player_punch.png")  
        self.player = self.canvas.create_image(50, 100, image=self.player_idle_image, anchor=NW)

        self.enemy_idle_image = PhotoImage(file="enemy_idle.png")  
        self.enemy_strike_image = PhotoImage(file="enemy_punch.png")  
        self.enemy = self.canvas.create_image(200, 100, image=self.enemy_idle_image, anchor=NW)

        self.player_hitpoints_bar = self.canvas.create_rectangle(30, 20, 30 + self.player_hitpoints * 2, 60, fill='green', outline='white')
        self.enemy_hitpoints_bar = self.canvas.create_rectangle(780 - self.enemy_hitpoints * 2, 20, 780, 60, fill='red', outline='white')

        self.entry_frame = Frame(self.root, bg='black')
        self.entry_frame.grid(row=4, column=0, columnspan=3, pady=(10, 5), sticky="ew")

        self.entry_frame.grid_columnconfigure(0, weight=1)
        self.entry_frame.grid_columnconfigure(1, weight=0)
        self.entry_frame.grid_columnconfigure(2, weight=1)

        self.answer_entry = Entry(self.entry_frame, textvariable=self.given_answer, font=('Times', 19), width=20)
        self.answer_entry.grid(row=0, column=0, padx=(10, 5), sticky="e")

        self.submit_button = Button(self.entry_frame, text="Submit", fg="#73e5ff", bg="#000000", font=('Times', 14), command=self.check_answer)
        self.submit_button.grid(row=0, column=1, padx=(5, 10), sticky="w")

        self.restart_button = Button(self.root, text="Restart", fg="red", font=('Times', 15), width=35, command=self.restart, bg='black', activebackground='black', activeforeground='red')
        self.restart_button.grid(row=5, column=0, columnspan=3, pady=(10, 20))

        self.result_label = Label(self.root, text="", font=('Times', 20), bg='black')
        self.result_label.grid(row=6, column=0, columnspan=3, pady=(10, 20))


        self.answer_entry.bind('<Return>', self.check_answer)

    def strike(self):
        self.canvas.delete(self.player)
        self.player = self.canvas.create_image(50, 100, image=self.player_strike_image, anchor=NW)

    def idle(self):
        self.canvas.delete(self.player)
        self.player = self.canvas.create_image(50, 100, image=self.player_idle_image, anchor=NW)

    def enemy_strike(self):
        self.canvas.delete(self.enemy)
        self.enemy = self.canvas.create_image(200, 100, image=self.enemy_strike_image, anchor=NW)

    def enemy_idle(self):
        self.canvas.delete(self.enemy)
        self.enemy = self.canvas.create_image(200, 100, image=self.enemy_idle_image, anchor=NW)

    def generate_question(self):
        self.quiz.question_number += 1
        question_text = self.quiz.generate_question()
        self.question.set(question_text)
        self.answer.set(self.quiz.current_answer)

        self.question_label.config(text=f"Question : {self.question.get()}")
        self.start_time = time.time()

        self.countdown()
        self.given_answer.set('')
        self.question_number_label.config(text=f"{self.quiz.question_number})")

    def countdown(self):
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = self.Question_Timer - elapsed_time

        if remaining_time <= 0:
            self.result_label.config(text="Time's up!", fg="red")
            self.generate_question()
            self.incorrect_answer()
        else:
            self.timer_label.config(text=f"Time left: {remaining_time} seconds")
            self.root.after(1000, self.countdown)

    def check_answer(self, event=None):
        try:
            user_answer = int(self.given_answer.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")
            return

        if self.quiz.check_answer(user_answer):
            self.quiz.increment_score()
            self.result_label.config(text="Correct", font=('Times', 20), fg="#76F984", bg='black')
            self.correct_answer()
        else:
            self.result_label.config(text="Incorrect", font=('Times', 20), fg="red", bg='black')
            self.incorrect_answer()

        self.score_label.config(text=f"Score : {self.quiz.score}")

        if self.enemy_hitpoints <= 0:
            self.show_end_screen(win=True)
        else:
            self.generate_question()

        self.given_answer.set('')

    def update_hitpoints_bars(self):
        self.canvas.coords(self.player_hitpoints_bar, 30, 20, 30 + self.player_hitpoints * 2, 60)
        self.canvas.coords(self.enemy_hitpoints_bar, 780 - self.enemy_hitpoints * 2, 20, 780, 60)

        if self.player_hitpoints <= 0:
            self.show_end_screen(win=False)

    def incorrect_answer(self):
        self.player_hitpoints -= 10  # Decrease player hitpoints
        self.update_hitpoints_bars()

        self.enemy_punched = False

        self.enemy_strike()
        self.move_enemy_forward()

    def correct_answer(self):
        self.enemy_hitpoints -= 10  # Decrease enemy hitpoints
        self.update_hitpoints_bars()

        self.punched = False

        self.strike()
        self.move_player_forward()

    def move_enemy_forward(self):
        self.canvas.move(self.enemy, -5, 0)

        x1, y1 = self.canvas.coords(self.enemy)

        if x1 > 150 and not self.enemy_punched:
            self.canvas.after(10, self.move_enemy_forward)
        else:
            self.move_enemy_backward()
            self.enemy_punched = True

    def move_enemy_backward(self):
        self.canvas.move(self.enemy, 5, 0)

        x1, y1 = self.canvas.coords(self.enemy)

        if x1 < 200:
            self.canvas.after(10, self.move_enemy_backward)
        else:
            self.enemy_idle()

    def move_player_forward(self):
        self.canvas.move(self.player, 5, 0)

        x1, y1 = self.canvas.coords(self.player)

        if x1 < 100 and not self.punched:
            self.canvas.after(10, self.move_player_forward)
        else:
            self.move_player_backward()
            self.punched = True

    def move_player_backward(self):
        self.canvas.move(self.player, -5, 0)

        x1, y1 = self.canvas.coords(self.player)

        if x1 > 50:
            self.canvas.after(10, self.move_player_backward)
        else:
            self.idle()

    def show_end_screen(self, win):
        self.root.withdraw()  # Hide the main window

        end_screen = Toplevel(self.root)
        end_screen.title("Game Over" if not win else "You Win!")
        end_screen.geometry("400x200")
        end_screen.configure(bg='black')

        message = "Congratulations, you won the game!" if win else "Sorry, you lost the game."
        message_label = Label(end_screen, text=message, font=('Times', 20), fg="#73e5ff", bg='black')
        message_label.pack(pady=20)

        restart_button = Button(end_screen, text="Play Again", font=('Times', 15), command=lambda: (end_screen.destroy(), self.restart()))
        restart_button.pack(pady=5)

        quit_button = Button(end_screen, text="Quit", font=('Times', 15), command=self.root.quit)
        quit_button.pack(pady=5)

    def restart(self):
        self.quiz.reset()
        self.player_hitpoints = 100
        self.enemy_hitpoints = 100
        self.update_hitpoints_bars()
        self.generate_question()
        self.score_label.config(text=f"Score : {self.quiz.score}")
        self.submit_button.config(state=NORMAL)
        self.question_number_label.config(text=f"{self.quiz.question_number})")
        self.canvas.coords(self.player, 50, 100)  # Reset player position
        self.canvas.coords(self.enemy, 200, 100)  # Reset enemy position
        self.root.deiconify()  # Show the main window again

class LoginPage:
    def __init__(self, root, on_success):
        self.root = root
        self.root.title("Login / Sign Up")
        self.root.geometry("450x400")
        self.root.configure(bg='black')

        self.on_success = on_success

        # UI Elements
        self.username = StringVar()
        self.password = StringVar()
        self.difficulty = StringVar(value='Easy')

        self.create_widgets()

    def create_widgets(self):
        self.heading_label = Label(self.root, text="Maths Quiz", font=('Times', 30), fg="#73e5ff", bg='black')
        self.heading_label.pack(pady=20)

        # Form frame
        self.form_frame = Frame(self.root, bg='black')
        self.form_frame.pack(pady=10)

        self.username_label = Label(self.form_frame, text="Username:", font=('Times', 15), fg="#73e5ff", bg='black')
        self.username_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.username_entry = Entry(self.form_frame, textvariable=self.username, font=('Times', 15))
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = Label(self.form_frame, text="Password:", font=('Times', 15), fg="#73e5ff", bg='black')
        self.password_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.password_entry = Entry(self.form_frame, textvariable=self.password, font=('Times', 15), show='*')
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.difficulty_label = Label(self.form_frame, text="Select Difficulty:", font=('Times', 15), fg="#73e5ff", bg='black')
        self.difficulty_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')

        difficulty_options = ['Easy', 'Medium', 'Hard']
        self.difficulty_menu = OptionMenu(self.form_frame, self.difficulty, *difficulty_options)
        self.difficulty_menu.config(font=('Times', 15), bg='black', fg="#73e5ff")
        self.difficulty_menu.grid(row=2, column=1, padx=5, pady=5)

        # Buttons frame
        self.button_frame = Frame(self.root, bg='black')
        self.button_frame.pack(pady=10)

        self.switch_button = Button(self.button_frame, text="Sign Up", font=('Times', 15), command=self.toggle_mode, fg="#73e5ff", bg="black", activebackground="black", activeforeground="#73e5ff")
        self.switch_button.grid(row=0, column=0, padx=10)

        self.action_button = Button(self.button_frame, text="Login", font=('Times', 15), command=self.login, fg="#73e5ff", bg="black", activebackground="black", activeforeground="#73e5ff")
        self.action_button.grid(row=0, column=1, padx=10)

        self.mode = StringVar(value='login')  # Default to login mode

    def load_users(self):
        try:
            with open('users.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print("No existing user file found. Creating a new one.")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error reading JSON file: {e}")
            return {}

    def save_users(self, users):
        try:
            with open('users.json', 'w') as file:
                json.dump(users, file, indent=4)
        except IOError as e:
            print(f"Error writing to JSON file: {e}")

    def toggle_mode(self):
        if self.mode.get() == 'login':
            self.show_signup()
        else:
            self.show_login()

    def show_login(self):
        self.mode.set('login')
        self.heading_label.config(text="Login")
        self.switch_button.config(text="Sign Up")
        self.action_button.config(text="Login", command=self.login)

    def show_signup(self):
        self.mode.set('signup')
        self.heading_label.config(text="Sign Up")
        self.switch_button.config(text="Login")
        self.action_button.config(text="Sign Up", command=self.signup)

    def login(self):
        username = self.username.get()
        password = self.password.get()
        selected_difficulty = self.difficulty.get()

        users = self.load_users()

        if username in users and users[username] == password:
            self.on_success(selected_difficulty)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def signup(self):
        username = self.username.get()
        password = self.password.get()

        if not username or not password:
            messagebox.showerror("Sign Up Failed", "Username and password cannot be empty")
            return

        users = self.load_users()

        if username in users:
            messagebox.showerror("Sign Up Failed", "Username already exists")
            return

        users[username] = password
        self.save_users(users)
        messagebox.showinfo("Sign Up Successful", "Account created successfully! You can now log in.")
        self.show_login()
def show_quiz(difficulty):
    root = Tk()
    app = MathQuizApp(root, difficulty)
    root.mainloop()

if __name__ == "__main__":
    root = Tk()
    login_page = LoginPage(root, on_success=lambda difficulty: (root.destroy(), show_quiz(difficulty)))
    root.mainloop()
