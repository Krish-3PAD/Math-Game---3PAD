# Program developed by Krish Patel.
# 2/09/2024.
# Program contains a mathematical quiz. 

import json  # Json used for data file storage. 
from tkinter import *
from tkinter import messagebox
from random import randint, choice
import time

class MathQuiz:  
    """
    Class creates the math quiz seen on the GUI. 

    """

    def __init__(self, difficulty):
        """
        Function used to start the intial program.

        Retrives difficulty from login page and assgins it to program.
        
        """


        self.difficulty = difficulty  # Assigns the users chosen difficulty to the Math QUiz object.
        self.score = 0  # Starts the Math Quiz with a score of 0.
        self.question_number = 0  # Sets the Question Number to zero at start of Math Quiz.
        self.start_time = 0  # Sets The intial time to 0, this assits in tracking the Quiz or indiviudal question start times.
        self.current_answer = None # Sets the starting answer to None, However will be assigned to the correct answer once question generates.
        self.set_difficulty() # Calls back on the set_difficulty function to set the quiz based on the difficulty selected. 

    def set_difficulty(self): 
        """
        Function Creates the set difficulties.

        Each difficulty has a range of numerical values for its operator. 
        
        """
        if self.difficulty == 'Easy':
            self.add_sub_range = (1, 10) # Creates numerical range for easy difficulties addition and subtraction.  
            self.mul_range = (1, 5) # Creates numerical range for easy difficulties multiplication. 
            self.div_range = (1, 5) # Creates numerical range for easy difficulties division.  
            self.operations = ['+', '-', '*', '/'] # Operators used in the easy difficulty.
            self.hitpoints_decrement = 10 # Hitpoints taken from the heath bar when a question is incorrectly answered.
        elif self.difficulty == 'Medium':
            self.add_sub_range = (1, 40) # Creates numerical range for medium difficulties addition and subtraction.
            self.mul_range = (5, 10) # Creates numerical range for medium difficulties multiplication
            self.div_range = (5, 10) # Creates numerical range for medium difficulties division. 
            self.operations = ['+', '-', '*', '/'] # Operators used in the medium difficulty.
            self.hitpoints_decrement = 10
        else: 
            self.add_sub_range = (1, 70) # Creates numerical range for medium difficulties addition and subtraction.
            self.mul_range = (7, 15) # Creates numerical range for medium difficulties multiplication
            self.div_range = (7, 15) # Creates numerical range for medium difficulties division. 
            self.operations = ['+', '-', '*', '/'] # Operators used in the Hard difficulty 
            self.hitpoints_decrement = 10

    def generate_question(self):
        """
        Generates a random question using the 4 different operations above. 

        """

        operator = choice(self.operations) # Selects an operator from the 4 given operations.
        
        if operator == '+': # Checks if the random operator chosen is additon +.
            number1 = randint(*self.add_sub_range) # First random number from the range of addition and subtraction values.
            number2 = randint(*self.add_sub_range) # Second random nubmer chosen within the range of values defined above. 
        elif operator == '-': # Checks if the random operator chosen for question is subtraction -. 
            number1 = randint(*self.add_sub_range) # First random nmber selected from range of subtraction/addition values. 
            number2 = randint(*self.add_sub_range) # Second random nmber selected from range of subtraction/addition values. 
        elif operator == '*': # Checks if the random operator chosen for question is multiplication *. 
            number1 = randint(*self.mul_range) # First random nmber selected from range of multiplication values. 
            number2 = randint(*self.mul_range) # Second random nmber selected from range of multiplication values. 
        elif operator == '/': # Checks if the random operator chosen is division /.
            number1 = randint(*self.div_range) # First random nmber selected from range of division values. 
            number2 = randint(*self.div_range) # Second random nmber selected from range of division values.
            if number2 == 0: # Checks if the denominator is 0
                number2 = 1 # Sets denominator to 1 if it is 0
            number1 = number2 * randint(1, 10)  # Ensures Quotient is an interger

        if operator == '+': # Checks if operator is addition to calculate answer.
            self.current_answer = number1 + number2 # Calculates answer for addition by adding number 1 and number 2..
        elif operator == '-':  # Checks if operator is subtraction fro answer calculation. 
            self.current_answer = number1 - number2 # Calculates answer for subtraction by subtracting number 1 by number 2..
        elif operator == '*': # Checks if operator is multiplication for an answer calculation. 
            self.current_answer = number1 * number2 # Calculates answer for addition by multiplying number 1 and number 2..
        elif operator == '/': # Checks if operator is division for an answer calculation.
            self.current_answer = number1 // number2 # Calculates answer for divison by dividing number 1 by number 2.

        question = f"{number1} {operator} {number2}" # Sets formating for question in the form of a string. 
        return question # Returns question formed. 

    def check_answer(self, user_answer): 
        """
        This function is used to check the users answer against the correct answer. 

        """
        return str(self.current_answer) == str(user_answer) # Converts answers to strings and compares them to check if User was correct. 

    def increment_score(self):
        """
        Increments score label by a single value. 

        """ 
        self.score += 1 # Increases the Users score by one. 

    def reset(self):
        """
        Resets the score and question number to intial value of zero

        """
        self.score = 0
        self.question_number = 0


class MathQuizApp: 
    '''
    This class creates the window for the math quiz app.

    Containing all the widjets and images. 

    '''
    Question_Timer = 10  # Sets the time limit for each question. 

    def __init__(self, root, difficulty):
        """
        Root sets sizing, colour and title of math quiz app window.

        Stores the diffuclty level chosen by the user.

        """

        self.root = root
        self.root.geometry("820x1000") # Sets Size of the Math Quizes window.
        self.root.title("MATHS MAYHEM") # Sets Title of the GUI window.
        self.root.configure(bg='black') # Sets the background to black.

        self.quiz = MathQuiz(difficulty) # Starts`` the Math Quiz window using chosen difficulty. 
        self.difficulty = difficulty # Stores the difficulty level. 
        self.game_over = False  # Add this to track if the game is over

    
        self.player_hitpoints = 100 # Sets inital hitpoints for player.
        self.enemy_hitpoints = 100 # Sets inital hitpoints for enemy. 

        self.question = StringVar() # String variable made to store the current question text. 
        self.answer = StringVar() # String variable made to store the answer to the current question. 
        self.given_answer = StringVar() # String variable made to store users inputted answer. 

        self.Widjets()
        self.generate_question()

    def Widjets(self):
        '''

        Creates the widgets to be placed onto the GUI.

        '''

        self.title_label = Label(self.root, text="MATHS MAYEM", font=('Times', 29), fg="#73e5ff", bg='black') # Creates Label for the title. 
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(20, 20)) # Sets title labels postion on User Interface by placing it on a grid.

        self.top_frame = Frame(self.root, bg='black') # Creating frame to store the question text, number and score labels. 
        self.top_frame.grid(row=1, column=0, columnspan=3, pady=(10, 20), sticky="ew") # Positions the frame on the User Interface.

        self.question_number_label = Label(self.top_frame, text=f"{self.quiz.question_number})", font=('Times', 19), fg="#73e5ff", bg='black') # Creating a label for the question number.
        self.question_number_label.grid(row=0, column=0, padx=(10, 5), sticky="e") # Positions the question nummber in the frame. 

        self.question_label = Label(self.top_frame, text="", font=('calibri', 19), bg='#73e5ff', fg='black') # Creates Label for the users score 
        self.question_label.grid(row=0, column=1, padx=(15, 5), sticky="nsew") # Positions the users score in the frame. 

        self.score_label = Label(self.top_frame, text=f"Score : {self.quiz.score}", font=('Times', 19), fg="#73e5ff", bg='black') 
        self.score_label.grid(row=0, column=2, padx=(10, 5), sticky="w")

        self.top_frame.grid_columnconfigure(0, weight=1) # Configures column weights for resizing. 
        self.top_frame.grid_columnconfigure(1, weight=1)
        self.top_frame.grid_columnconfigure(2, weight=1)

        self.timer_label = Label(self.root, text="", font=('Times', 19), fg="#73e5ff", bg='black') # Creates a label for the 10 second question timer. 
        self.timer_label.grid(row=2, column=0, columnspan=3, pady=(15, 20)) # Sets the position for the timer on the User Interface. 

        self.canvas = Canvas(self.root, width=815, height=535, bg='purple') # Creates Canvas to implement Images (game aspect).
        self.canvas.grid(row=3, column=0, columnspan=3, pady=(10, 20)) # Sets position of Canvas on the User Interface. 

        self.background_image = PhotoImage(file="background.png") # Loads the background image. 
        self.background = self.canvas.create_image(400, 300, image=self.background_image, anchor=CENTER) # Positions the background image on the canvas. 

        self.player_idle_image = PhotoImage(file="player_idle.png") # Loads up the image for the users fighter/character. 
        self.player_strike_image = PhotoImage(file="player_punch.png")  # Loads Up image for the users fighter/character striking. 
        self.player = self.canvas.create_image(50, 100, image=self.player_idle_image, anchor=NW) # Positions the users fighter on the canvas. 

        self.enemy_idle_image = PhotoImage(file="enemy_idle.png") # Loads up the image for the enemies fighter/character.  
        self.enemy_strike_image = PhotoImage(file="enemy_punch.png") # Loads Up image for the enemies fighter/character striking.
        self.enemy = self.canvas.create_image(200, 100, image=self.enemy_idle_image, anchor=NW) # Positions the enemy fighter on the canvas.

        self.player_hitpoints_bar = self.canvas.create_rectangle(30, 20, 30 + self.player_hitpoints * 2, 60, fill='green', outline='white') # Creates the Users health bar.
        self.enemy_hitpoints_bar = self.canvas.create_rectangle(780 - self.enemy_hitpoints * 2, 20, 780, 60, fill='red', outline='white') # Creates the enemies health bar. 

        self.entry_frame = Frame(self.root, bg='black') # Creates the frame for users inputted answers with a black background colour. 
        self.entry_frame.grid(row=4, column=0, columnspan=3, pady=(10, 5), sticky="ew") # Positions the frame in the user interface. 

        self.entry_frame.grid_columnconfigure(0, weight=1) # Sets the column widths within the frame. 
        self.entry_frame.grid_columnconfigure(1, weight=0)
        self.entry_frame.grid_columnconfigure(2, weight=1)

        self.answer_entry = Entry(self.entry_frame, textvariable=self.given_answer, font=('Times', 19), width=20) # Creates an entry field for the user to answer.
        self.answer_entry.grid(row=0, column=0, padx=(10, 5), sticky="e") # Sets the position for the entry field on the user interface. 

        self.submit_button = Button(self.entry_frame, text="Submit", fg="#73e5ff", bg="#000000", font=('Times', 14), command=self.check_answer) # Creates a Submit button for user to submit answers.
        self.submit_button.grid(row=0, column=1, padx=(5, 10), sticky="w") # Sets the position of the submit button on the user interface. 

        self.restart_button = Button(self.root, text="Restart", fg="red", font=('Times', 15), width=35, command=self.restart, bg='black', activebackground='black', activeforeground='red') # Creates a restart button.
        self.restart_button.grid(row=5, column=0, columnspan=3, pady=(10, 20)) # Sets the position of the restart button on the user interface. 

        self.result_label = Label(self.root, text="", font=('Times', 20), bg='black') # Creates a label for the result. 
        self.result_label.grid(row=6, column=0, columnspan=3, pady=(10, 20)) # Positions the result label bellow the restart button.


        self.answer_entry.bind('<Return>', self.check_answer)

    def strike(self):

        """
        Replaces player idle image with a player striking image. 

        """
        
        if self.game_over: return  # Stops if the game is over.
        self.canvas.delete(self.player) # Removes player_idle image. 
        self.player = self.canvas.create_image(50, 100, image=self.player_strike_image, anchor=NW) # Displays the player_strike image. 

    def idle(self): 
        """
        Function used to set the fighter back to an idel positon

        """

        if self.game_over: return  # Stops if the game is over.
        self.canvas.delete(self.player) # Deletes the current player_figheters image. 
        self.player = self.canvas.create_image(50, 100, image=self.player_idle_image, anchor=NW) # Displays the player_idle image. 


    def enemy_strike(self):
        """
        Function used to replace enemy idle image with enemy strike.  
        
        """  
         
        if self.game_over: return  # Stops if the game is over.
        self.canvas.delete(self.enemy) # Deletes current enemy fighters image. 
        self.enemy = self.canvas.create_image(200, 100, image=self.enemy_strike_image, anchor=NW) # Displays the enemy striking image.


    def enemy_idle(self): 
        """
        Function used to set enemy image back to enemy_idle.

        """

        if self.game_over: return  # Stop if the game is over.
        self.canvas.delete(self.enemy) # Deletes current enemy image. 
        self.enemy = self.canvas.create_image(200, 100, image=self.enemy_idle_image, anchor=NW) # Displays the enemy idle image. 

    def generate_question(self):
        """
        Generates a new question after question is answered. 
        
        """

        if self.game_over: return  # Stop generating questions if the game is over.
        self.quiz.question_number += 1 # Incraments the question number attribute by one for a new question to be generated. 
        question_text = self.quiz.generate_question() # Calls back on generate_question function for a new question. 
        self.question.set(question_text) # Adds new question text by updating question variable. 
        self.answer.set(self.quiz.current_answer) # Sets the answer to the question to the correct current answer for the question.

        self.question_label.config(text=f"Question : {self.question.get()}") # Updates question label to show the new question. 
        self.start_time = time.time()

        self.countdown() # Starts the timer countdown for the question displayed. 
        self.given_answer.set('') # Clears the previous input made by the user. 
        self.question_number_label.config(text=f"{self.quiz.question_number})") # Changes the label of the question number to show the new question number. 

    def countdown(self):
        """
        Function used to manipulate the timer on the math quiz
        
        """

        if self.game_over: return  # Stops the countdown if the game is over.

        elapsed_time = int(time.time() - self.start_time) # Used to calculate the time passed since timer started. 
        remaining_time = self.Question_Timer - elapsed_time

        if remaining_time <= 0: # Checks to see if the timer has hit zero.
            self.result_label.config(text="Time's up!", fg="red") # If condition is true "times up" is printed onto the GUI. 
            self.generate_question() # A new question is generated as the time has ran out. 
            self.incorrect_answer() # Ad
        else:
            self.timer_label.config(text=f"Time left: {remaining_time} seconds") # Changes the timer label with the remaining_time.
            self.root.after(1000, self.countdown) # Countdown fucntion is called again after 1000 miliseconds. 

    def check_answer(self, event=None):
        """
        Runs validation check on user inputted answer

        Checks if the enemy health bar has been depleated to display an end screen.

        """

        if self.game_over: return  # Stop checking answers if the game is over

        try:
            user_answer = int(self.given_answer.get()) # Tries to convert the Users input into an interger. 
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer") # Error box pops up if inputted data is not converted to an interger. 
            return

        if self.quiz.check_answer(user_answer): # Checks to see if the user succsesfully answered the question correctly. 
            self.quiz.increment_score() # If answer is correct the score is incremented. 
            self.result_label.config(text="Correct", font=('Times', 20), fg="#76F984", bg='black') # Changes label used to indicate to the User that they were correct 
            self.correct_answer()
        else:
            self.result_label.config(text="Incorrect", font=('Times', 20), fg="red", bg='black') # If users answer was incorrect result label is updated to show incorrect. 
            self.incorrect_answer() # This fucntion will deal with the incorrect answer. 

        self.score_label.config(text=f"Score : {self.quiz.score}") # Changes the score label to show the current score. 

        if self.enemy_hitpoints <= 0: # Checks if the enemy fighter health bar has depleated 
            self.show_end_screen(win=True) # If enemy fighter health bar has depleated ending win screen is displayed.
        elif self.player_hitpoints <= 0: # Checks if Users health bar has depleated. 
            self.show_end_screen(win=False)# If Users health bar has depleated ending losing screen is displayed.
        else:
            self.generate_question() # If neither health bar is depleated game conintues with a new question generated. 

        self.given_answer.set('') # Clears any inputs/entries made by the user from the previous quesiton. 


    def update_hitpoints_bars(self):
        """
        Updates the enemies and players health bar after each question. 

        Sets sizing of the player and enemy health bar. 

        """

        self.canvas.coords(self.player_hitpoints_bar, 30, 20, 30 + self.player_hitpoints * 2, 60) # Adds any changes to the size of the users health bar.
        self.canvas.coords(self.enemy_hitpoints_bar, 780 - self.enemy_hitpoints * 2, 20, 780, 60) # Adds any changes to the size of the enemies health bar.

        if self.player_hitpoints <= 0: # Checks if users health bar is greater than or equal to zero (depleaded).
            self.show_end_screen(win=False) # Displays losing screen if Users health bar has depleated.
        

    def incorrect_answer(self):
        """
        Causes health bar to decrease when answer is incorrectly answered.
    
        """
        self.player_hitpoints -= 10  # Decreases the players hitpoints by 10.
        self.update_hitpoints_bars()  # Updates the hitpoints bars on the canvas.

        self.enemy_punched = False  # Reset the flag indicating that the enemy was punched.

        self.enemy_strike()  # Activates the enemy striking animation.
        self.move_enemy_forward()  # Move the enemy forward for the strike. 

    def correct_answer(self):   
        """
        Decreases enemy health bar when question is answered correcty.
        """

        self.enemy_hitpoints -= 10  # Decreases the enemies hitpoints by 10.
        self.update_hitpoints_bars()  # Update the hitpoints bars on the canvas.

        self.punched = False  # Reset the flag indicating that the player was punched.

        self.strike()  # Activates the player attacking animation. 
        self.move_player_forward()  # Moves the player forward for a strike. 
    
    
    def move_enemy_forward(self):
        """
         animation which moves enemy character forward for a strike. 

        """
        if self.game_over: return  # Stops the enemy's movement if the game is over.

        self.canvas.move(self.enemy, -5, 0)  # Moves the enemy character 5 pixels to the left.

        x1, y1 = self.canvas.coords(self.enemy)  # Gets the current coordinates of the enemy.

        if x1 > 150 and not self.enemy_punched:  # Checks if the enemy should continue moving forward.
            self.canvas.after(10, self.move_enemy_forward)
        else:
            self.move_enemy_backward()  # Moves the enemy back after the punch.
            self.enemy_punched = True  # Sets flag to indicate the enemy has punched.

    def move_enemy_backward(self):
        """
         animation which moves enemy player backwards after strike is complete.

        """
        if self.game_over: return # Stops the enemy's movement if the game is over.

        self.canvas.move(self.enemy, 5, 0) # Moves the enemy character 5 pixels to the right.

        x1, y1 = self.canvas.coords(self.enemy) # Gets the current coordinates of the enemy.

        if x1 < 200: # Checks if the enemy should continue moving backward.
            self.canvas.after(10, self.move_enemy_backward)
        else:
            self.enemy_idle() # Sets the enemy to idle once it has moved back to its position.

    def move_player_forward(self):
        """
        animation which moves player forward for a strike.

        """

        if self.game_over: return # Stops the player's movement if the game is over.

        self.canvas.move(self.player, 5, 0) # Moves the player character 5 pixels to the right.

        x1, y1 = self.canvas.coords(self.player) # Gets the current coordinates of the player.

        if x1 < 100 and not self.punched:  # Checks if the player should continue moving forward.
            self.canvas.after(10, self.move_player_forward)
        else:
            self.move_player_backward() # Moves the player back after the punch.
            self.punched = True # Sets flag to indicate the player has punched.

    def move_player_backward(self):
        """
        animation which moves player back after striking.

        """
        if self.game_over: return # Stops the player's movement if the game is over.

        self.canvas.move(self.player, -5, 0) # Moves the player character 5 pixels to the left.

        x1, y1 = self.canvas.coords(self.player) # Gets the current coordinates of the player.

        if x1 > 50: # Checks if the player should continue moving backward.
            self.canvas.after(10, self.move_player_backward)
        else:
            self.idle() # Set the player to idle once it has moved back to its position.


    def show_end_screen(self, win):
        """
        Function used to create the end screen if user wins or loses.

        """   
    
        if self.game_over: return  # Stops if the end screen has already been shown.
        
        self.game_over = True  # Sets the game_over flag to True, indicating the game has ended.

        self.root.withdraw()  # Hides the main game window.

        end_screen = Toplevel(self.root)  # Create a new window for the end screen.
        end_screen.title("Game Over" if not win else "You Win!")  # Set the title based on whether the player won or lost.
        end_screen.geometry("400x200")  # Sest the dimensions of the end screen window.
        end_screen.configure(bg='black')  # Sets the background color of the end screen to black.

        message = "Congratulations, you won the game!" if win else "Sorry, you lost the game."  # Set the message based on the game result.
        message_label = Label(end_screen, text=message, font=('Times', 20), fg="#73e5ff", bg='black')  # Create a label with the message.
        message_label.pack(pady=20)  # Adds padding around the message label and pack it into the window.

        restart_button = Button(end_screen, text="Play Again", font=('Times', 15), command=lambda: (end_screen.destroy(), self.restart()))  
        restart_button.pack(pady=5)  # Creates and pack a "Play Again" button with padding. It restarts the game when clicked.

        quit_button = Button(end_screen, text="Quit", font=('Times', 15), command=self.root.quit)  
        quit_button.pack(pady=5) # Creates and pack a "Quit" button with padding. It exits the game when clicked.



    def restart(self):
        """
        Resets widgets back to starting positions. 
        
        """   
        
        self.quiz.reset() # Resets the quiz for strating a new game.
        self.player_hitpoints = 100 # Resets player's hitpoints back to full.
        self.enemy_hitpoints = 100 # Resets enemy's hitpoints back to full.
        self.game_over = False # Resets the game_over flag when restarting.
        self.update_hitpoints_bars() # Updates the hitpoints bars to reflect the reset values.
        self.generate_question() # Generates a new question for the quiz.
        self.score_label.config(text=f"Score : {self.quiz.score}")  # Updates the score label with the reset score.
        self.submit_button.config(state=NORMAL) # Re-enables the submit button.
        self.question_number_label.config(text=f"{self.quiz.question_number})")  # Update the question number label.
        self.canvas.coords(self.player, 50, 100) # Resets player's position on the canvas.
        self.canvas.coords(self.enemy, 200, 100) # Resets enemy's position on the canvas.
        self.root.deiconify() # Shows the main window again after restarting.

class LoginPage:
    """
    This Class is used to create the login page
    """

    def __init__(self, root, on_success):
        """
        Sets sizng, background colour and title for login page.
        
        """
        self.root = root # Main application window.
        self.root.title("Login / Sign Up") # Sets the windows title.
        self.root.geometry("450x400") # Sets the windows size.
        self.root.configure(bg='black') # Sets the background colour.

        self.on_success = on_success # Callback function for successful login/signup.

        self.username = StringVar()  # Variable used to store username input.
        self.password = StringVar()  # Variable to used  store password input.
        self.difficulty = StringVar(value='Easy') # Variable used to store selected difficulty.

        self.create_widgets()  # Create and display UI elements.

    def create_widgets(self):
        """
        Function to create widgets for GUI.

        """

        self.heading_label = Label(self.root, text="""Welcome To....
MATH MAYHEM""", font=('Times', 30), fg="#73e5ff", bg='black')  # Sets a heading label for login page, Multline str for the heading.  
        self.heading_label.pack(pady=20)  # Adds the heading in the GUI in a set position. 

        
        self.form_frame = Frame(self.root, bg='black')  # Frame for form widgets, with black background. 
        self.form_frame.pack(pady=10)  # Adds the frame to the GUI in a set position (using vertical padding).

        self.username_label = Label(self.form_frame, text="Username:", font=('Times', 15), fg="#73e5ff", bg='black')  # Creates the username label for the username entry box.
        self.username_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')  # Sets positioning of the username window on the GUI adjacent to the entry box. 
        self.username_entry = Entry(self.form_frame, textvariable=self.username, font=('Times', 15))  # Creates entry box for users to input their usernames. 
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)  # Sets poisition of the entry box adjacvent to the username label.

        self.password_label = Label(self.form_frame, text="Password:", font=('Times', 15), fg="#73e5ff", bg='black')  # Creates the password label for the username entry box.
        self.password_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')  # Sets positioning of the password window on the GUI adjacent to the entry box. 
        self.password_entry = Entry(self.form_frame, textvariable=self.password, font=('Times', 15), show='*')  # Creates entry box for users to input their passwords. 
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)  # Sets poisition of the entry box adjacvent to the password label.

        self.difficulty_label = Label(self.form_frame, text="Select Difficulty:", font=('Times', 15), fg="#73e5ff", bg='black')
        self.difficulty_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')  # Difficulty label

        difficulty_options = ['Easy', 'Medium', 'Hard']  # Defines a list of difficulty options for the dropdownbox.
        self.difficulty_menu = OptionMenu(self.form_frame, self.difficulty, *difficulty_options)  # Creates the dropdown box for the range of difficulties. 
        self.difficulty_menu.config(font=('Times', 15), bg='black', fg="#73e5ff")  # Gives font style, size and colour for the dropdownbox.
        self.difficulty_menu.grid(row=2, column=1, padx=5, pady=5)  # Difficulty dropdown menu.


        self.button_frame = Frame(self.root, bg='black')  # Creates frame for buttons.
        self.button_frame.pack(pady=10)  # Adds the frame to the GUI and sets its position.

        self.switch_button = Button(self.button_frame, text="Press to Sign Up", font=('Times', 15), command=self.toggle_mode, fg="#73e5ff", bg="black", activebackground="black", activeforeground="#73e5ff")  # Creates a button for user to between logging in and signing up.
        self.switch_button.grid(row=0, column=0, padx=10)  # Sets Positioning of this button on the GUI. 

        self.action_button = Button(self.button_frame, text="Login", font=('Times', 15), command=self.login, fg="#73e5ff", bg="black", activebackground="black", activeforeground="#73e5ff") # Creates a button 
        self.action_button.grid(row=0, column=1, padx=10)  # Login/Sign Up action button

        self.mode = StringVar(value='login')  # Default to login mode

    def load_users(self):
        """
        Function used to load users from JSON file.
        """

        try:
            with open('users.json', 'r') as file:
                return json.load(file)  # Load existing users from file
        except FileNotFoundError:
            print("No existing user file found. Creating a new one.")  # Notify if file not found.
            return {}
        except json.JSONDecodeError as e:
            print(f"Error reading JSON file: {e}")  # Notify if there's an error reading JSON.
            return {}

    def save_users(self, users):
        """
        Function used to save users to JSON file.

        """

        try:
            with open('users.json', 'w') as file:
                json.dump(users, file, indent=4)  # Save users to file.
        except IOError as e:
            print(f"Error writing to JSON file: {e}")  # Notify if there's an error writing to file.

    def toggle_mode(self):
        """
        Function used to switch from sign up mode to login mode vice versa
        """
        if self.mode.get() == 'login':
            self.show_signup()  # Switch to sign up mode.
        else:
            self.show_login()  # Switch to login mode.

    def show_login(self):
        """
        Creates swtich button from login mode to sign up mode
        
        """

        self.mode.set('login')  # Set mode to login.
        self.heading_label.config(text="Login")  # Update heading label.
        self.switch_button.config(text="Press to Sign Up")  # Button used to switch to sign p mode.
        self.action_button.config(text="Login", command=self.login)  # Update action button text and command.

    def show_signup(self):
        """
        Creates swtich button for sign up mode to login mode
        
        """

        self.mode.set('signup')  # Set mode to sign up.
        self.heading_label.config(text="Sign Up")  # Update heading label.
        self.switch_button.config(text="Press to Login")  # Button used to switch to login mode. 
        self.action_button.config(text="Sign Up", command=self.signup)  # Update action button text and command.

    def login(self):
        """
        Function to retrive inputted username, password and selected. 

        Checks if the login is valid

        """

        username = self.username.get()  # Retrives entered username.
        password = self.password.get()  # Retrives entered password.
        selected_difficulty = self.difficulty.get()  # Retrives selected difficulty.

        users = self.load_users()  # Load users from file.

        if username in users and users[username] == password:
            self.on_success(selected_difficulty)  # Successful login.
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")  # Show error if login fails.

    def signup(self):
        
        """
        Function runs validation checks on sign up inputs. 
        
        """
        username = self.username.get()  # Get entered username.
        password = self.password.get()  # Get entered password.
        
        if not username or not password:
            messagebox.showerror("Sign Up Failed", "Username and/or password cannot be empty")  # Error box occurs if fields are empty.
            return
        
        
        
        if len(username) > 10:
            messagebox.showerror("Sign Up Failed", "Username cannot be greater than 10 characters long")  # Error box occurs if username is too long.
            return

        for letters in username:
            if not letters.isalpha():
                messagebox.showerror("Sign Up Failed", "Please only use letters for your username")  # Error box occurs if username contains non-letter characters.
                return

        users = self.load_users()  # Loads users saved from JSON file.

        if username in users:
            messagebox.showerror("Sign Up Failed", "Username already in use")  # Error box occurs if username is already taken.
            return

        users[username] = password  # Adds a new user.
        self.save_users(users)  # Save updated user list.
        messagebox.showinfo("Sign Up Successful", "Account created successfully! You can now log in.")  # Notify user of successful sign up.
        self.show_login()  # Switch to login mode.

def main():  
    """
    Function used to create main tkinter window.
    
    """ 
    def show_quiz(difficulty):
        root = Tk()  # Create new Tkinter root window
        app = MathQuizApp(root, difficulty)  # starts the quiz app with the selected difficulty
        root.mainloop()  # Run the Tkinter event loop

    if __name__ == "__main__":
        root = Tk()  # Create main Tkinter window
        login_page = LoginPage(root, on_success=lambda difficulty: (root.destroy(), show_quiz(difficulty)))  # starts login page with success callback
        root.mainloop()  # Run the Tkinter event loop

main()  # Calls back on main function. 
