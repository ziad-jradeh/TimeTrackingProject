from time import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

from classes import *
import shutil
import json

# The path for the json file that contains all the data.
data_file = "data/data.json"

backup_file = "data/data.backup.json" # The path to the backup data file.

# A global list that will contain all the users objects
users_list = []

class LoginUI(QDialog):
    def __init__(self):
        super(LoginUI,self).__init__()
        loadUi("./UI/login.ui",self)
        
        # for easy testing, you can log in with this email easily. to be removed later
        self.emailInputLogin.setText("john@gmail.com")
        
        # Read the data from the json, if the file is corrupted, read the backup file.
        global json_data
        try:
            with open(data_file, "r") as f:
                json_data = json.load(f)
        except:
            with open(backup_file, "r") as f:
                json_data = json.load(f)
                
        global users_list
        
        # Fill the users list with all the users objects from the json file after converting them into User objects.
        # same as:
        # for user_dict in json_data:
        #     users_list.append(dict_to_user(user_dict))
        users_list = [dict_to_user(user_dict) for user_dict in json_data]
        
        # Define the handler functions for the login and sign up buttons.
        self.loginButton.clicked.connect(self.login)
        self.signUpButton.clicked.connect(self.signUp)
        
        
    def login(self):
        '''A handler function for the login button click event.'''
        
        email = self.emailInputLogin.text()     # read the email the user entered
        
        # Search for the user with the input email, if found, it is the current user and go to main menu.
        for user in users_list:
            if email == user.email:
                global current_user
                current_user = user
                self.go_main_menu()
                return
        # if the email was not found, show an error message.
        self.errorTextLogin.setText(f"No account for {email}, please sign up first.")
    
    def signUp(self):
        '''A handler function for the sign up button click event.'''
        
        # read the name and email the user entered.
        name = self.nameInputSignUp.text()
        email = self.emailInputSignUp.text()
        
        # search for the email in the users list, if found, show an error message.
        for user in users_list:
            if email == user.email:
                self.errorTextSignUp.setText("Email already registered. please log in.")
                return
        # if the name field is empty, show an error message.
        if name == None:
            self.errorTextSignUp.setText("Name cannot be empty.")
            return
            
        # if the email is not found in the users list, create a new account.
        user = User(name, email)
        # add the account to the users list
        users_list.append(user)
        self.errorTextSignUp.setText("Account created for " + user.email + " You can now login")
        
        # Write the new users list to the json data file.
        save_data()
        
    

    def go_main_menu(self):
        main_menu = MainMenuUI()
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)


class MainMenuUI(QDialog):
    def __init__(self):
        super(MainMenuUI,self).__init__()
        loadUi("./UI/mainMenu.ui",self)

class PomodoroUI(QDialog):
    def __init__(self):
        super(PomodoroUI,self).__init__()
        loadUi("./UI/pomodoro.ui",self)


class ShortBreakUI(QDialog):
    def __init__(self):
        super(ShortBreakUI,self).__init__()
        loadUi("./UI/shortBreak.ui",self)

class LongBreakUI(QDialog):
    def __init__(self):
        super(LongBreakUI,self).__init__()
        loadUi("./UI/longBreak.ui",self)

def save_data():
    '''A function that saves the data for all the users in a json file.
    Also creates a backup copy before.'''
    # backup the data file, in case the used file becomes corrupted.
    shutil.copyfile(data_file, backup_file)
    
    # Convert the users list to dictionaries and save it to the json data file.
    with open(data_file, 'w') as f:
        json.dump(users_list, f, indent=4, cls= JsonEncoder)


app = QApplication(sys.argv)
UI = LoginUI() # This line determines which screen you will load at first

# You can also try one of other screens to see them.
    # UI = MainMenuUI()
    # UI = PomodoroUI()
    # UI = ShortBreakUI()
    # UI = LongBreakUI()

widget = QtWidgets.QStackedWidget()
widget.addWidget(UI)
widget.setFixedWidth(800)
widget.setFixedHeight(600)
widget.setWindowTitle("Time Tracking App")
widget.show()
sys.exit(app.exec_())
