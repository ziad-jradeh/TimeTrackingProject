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
        users_list = [Struct(user_dict) for user_dict in json_data]
        
        self.errorTextLogin.clear()
        self.errorTextSignUp.clear()

        
        # Define the handler functions for the login and sign up buttons.
        self.loginButton.clicked.connect(self.login)
        self.signUpButton.clicked.connect(self.signUp)
        
        
        
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
 
    def login(self):
        '''A handler function for the login button click event.'''
        
        email = self.emailInputLogin.text()     # read the email the user entered
        
        # Search for the user with the input email, if found, it is the current user and go to main menu.
        for user in users_list:
            if user.email == email:
                global current_user
                current_user = user
                self.go_main_menu()
                return
        # if the email was not found, show an error message.
        self.errorTextLogin.setText(f"No account for {email}, please sign up first.")
    
    
        
    

    def go_main_menu(self):
        main_menu = MainMenuUI()
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)


class MainMenuUI(QDialog):
    counter = 0
    current_project = ""
    current_subject = ""
    def __init__(self):
        super(MainMenuUI,self).__init__()
        loadUi("./UI/mainMenu.ui",self)
        # Set the addRecipientButton and deleteRecipientButton click event handlers.
        self.addRecipientButton.clicked.connect(self.add_recipient)
        self.deleteRecipientButton.clicked.connect(self.delete_recipient)
        self.addProjectButton.clicked.connect(self.add_project)
        self.projectDeleteButton.clicked.connect(self.delete_project)
        self.addSubjectButton.clicked.connect(self.add_subject)
        self.subjectDeleteButton.clicked.connect(self.delete_subject)
        self.startPomodoroButton.clicked.connect(self.go_pomodro)    

        # Load the recipients emails to the deleteRecipientCombo after clearing it.
        self.deleteRecipientCombo.clear()
        self.deleteRecipientCombo.addItems([recipient.email for recipient in current_user.recipients])
        
        self.projectDeleteCombo.clear()
        self.projectDeleteCombo.addItems([project.name for project in current_user.projects])
        
        
        self.selectProjectCombo.clear()
        self.selectProjectCombo.addItems([project.name for project in current_user.projects])
        
        
        self.addSubjectOnProjectCombo.clear()
        self.addSubjectOnProjectCombo.addItems([project.name for project in current_user.projects])
        
        self.selectSubjectCombo.clear()
        self.selectProjectCombo.activated.connect(self.check_index)
        selected_index = self.addSubjectOnProjectCombo.currentIndex()
        
        self.projectDeleteCombo.activated.connect(self.check_index2)
        # self.addSubjectOnProjectCombo.activated.connect(self.check_index)
        
        
        self.subjectDeleteCombo.clear()
        self.subjectDeleteCombo.addItems([subject.name for subject in current_user.projects[selected_index].subjects])
        
        self.errorTextRecipientsEmailLabel.clear()
        self.errorTextProjectLabel.clear()
        self.errorTextSubjectLabel.clear()
        self.showSummarySubjectCombo.clear()
        
        self.showSummaryProjectCombo.clear()
        self.showSummaryProjectCombo.addItems([project.name for project in current_user.projects])
        self.showSummaryProjectCombo.activated.connect(self.check_index3)
        
        

        
    
    def check_index(self, index):
        self.selectSubjectCombo.clear()
        self.selectSubjectCombo.addItems([subject.name for subject in current_user.projects[index].subjects])
        
    def check_index2(self, index):
        self.subjectDeleteCombo.clear()
        self.subjectDeleteCombo.addItems([subject.name for subject in current_user.projects[index].subjects])
        
    def check_index3(self, index):
        self.showSummarySubjectCombo.clear()
        self.showSummarySubjectCombo.addItems([subject.name for subject in current_user.projects[index].subjects])
        
        

    
        
        # Load the projects to the deleteProjectCombo after clearing it.
    def add_recipient(self):
        '''A handler function for the add recipient button click event.'''
        email = self.addRecipientInput.text()   # Get the recipient email the user entered
        # Check if it is already in the recipient list.
        if email == "":
            self.errorTextRecipientsEmailLabel.setText("This field cannot be empty.")
            return
        elif email in [i.email for i in current_user.recipients]:
            self.errorTextRecipientsEmailLabel.setText(f"{email} is already in the recipients list.")
        else:
            # Create a new Recipient from the email the user has entered and add it to recipients list and the recipients menu.
            recipient = Recipient(email)
            current_user.recipients.append(recipient)
            self.deleteRecipientCombo.addItem(recipient.email)
            self.deleteRecipientCombo.setCurrentIndex(len(current_user.recipients)-1)   # Select the new recipient in the menu (last one)
            self.errorTextRecipientsEmailLabel.setText(f"{email} is added to the recipients list.")
            save_data()
        
    def delete_recipient(self):
        '''A handler function for the delete recipient button click event.'''
        selected_index = self.deleteRecipientCombo.currentIndex()   # get the index of the selected recipient
        del current_user.recipients[selected_index]         # Delete the recipient from the recipients list
        self.deleteRecipientCombo.removeItem(selected_index)    # remove it from the recipients menu
        save_data()
    
    def add_project(self):
        project = self.addProjectInput.text()
        if project == "":
            self.errorTextProjectLabel.setText("This field cannot be empty.")
            return
        elif project in [i.name for i in current_user.projects]:
            self.errorTextProjectLabel.setText(f"{project} is already in the recipients list.")
        else:
            project_name = Project(project)
            MainMenuUI.current_project2 = project_name

            current_user.projects.append(project_name)
            self.projectDeleteCombo.addItem(project_name.name)
            self.projectDeleteCombo.setCurrentIndex(len(current_user.projects)-1)   # Select the new recipient in the menu (last one)
            self.addSubjectOnProjectCombo.addItem(project_name.name)
            self.addSubjectOnProjectCombo.setCurrentIndex(len(current_user.projects)-1)   # Select the new recipient in the menu (last one)
            self.selectProjectCombo.addItem(project_name.name)
            self.selectProjectCombo.setCurrentIndex(len(current_user.projects)-1)   # Select the new recipient in the menu (last one)
            self.errorTextProjectLabel.setText(f"{project} has been added.")
            save_data()
            
            
    def delete_project(self):
        '''A handler function for the delete recipient button click event.'''
        selected_index = self.projectDeleteCombo.currentIndex()   # get the index of the selected recipient
        del current_user.projects[selected_index]       # Delete the recipient from the recipients list
        self.projectDeleteCombo.removeItem(selected_index)    # remove it from the recipients menu
        self.selectProjectCombo.setCurrentIndex(selected_index)   # Select the new recipient in the menu (last one)
        self.selectProjectCombo.removeItem(selected_index)
        self.addSubjectOnProjectCombo.setCurrentIndex(selected_index)
        self.addSubjectOnProjectCombo.removeItem(selected_index)
        save_data()
    
    def add_subject(self):
        subject = self.addSubjectInput.text()
        selected_index_sbject = self.addSubjectOnProjectCombo.currentIndex()
        
        if subject == "":
            self.errorTextSubjectLabel.setText("This field cannot be empty.")

        elif subject in [i.name for i in current_user.projects for i in i.subjects]:
            self.errorTextSubjectLabel.setText(f"{subject} is already in the project.")
            
        else:
            subject_name = Subject(subject)
            MainMenuUI.current_subject2 = subject_name
            current_user.projects[selected_index_sbject].subjects.append(subject_name)
            self.errorTextSubjectLabel.setText(f"{subject} has been added.")
            save_data()
             
        
        
    def delete_subject(self):
        selected_index2 = self.projectDeleteCombo.currentIndex()
        selected_index = self.subjectDeleteCombo.currentIndex()
        del current_user.projects[selected_index2].subjects[selected_index]
        self.subjectDeleteCombo.removeItem(selected_index)    # remove it from the recipients menu
        save_data()

   


    def go_pomodro(self):
        Pomodoro_Session = PomodoroUI()
        widget.addWidget(Pomodoro_Session)
        MainMenuUI.counter = 0
        widget.setCurrentIndex(widget.currentIndex()+1)
        index1 = self.selectProjectCombo.currentIndex()
        index2 = self.selectSubjectCombo.currentIndex()
        
        a = self.selectProjectCombo.currentText()
        b = self.selectSubjectCombo.currentText()
        MainMenuUI.current_subject = a
        MainMenuUI.current_project = b
        
        if current_user.projects[index1].subjects[index2].PomodoroSessions:
            current_session = current_user.projects[index1].subjects[index2].PomodoroSessions[-1].number
            if  current_session >= MainMenuUI.counter:
                MainMenuUI.counter += 1
                MainMenuUI.counter += current_session
                pomo_session = PomodoroSessions(MainMenuUI.counter)
                current_user.projects[index1].subjects[index2].PomodoroSessions.append(pomo_session)
                # current_pomodro.append(pomo_session)
                save_data()
        else:
            MainMenuUI.counter += 1
            pomo_session = PomodoroSessions(MainMenuUI.counter)
            current_user.projects[index1].subjects[index2].PomodoroSessions.append(pomo_session)
            print(MainMenuUI.counter)
            # current_pomodro.append(pomo_session)
            save_data()
        # print(MainMenuUI.current_project,MainMenuUI.current_subject)
        
        
class PomodoroUI(QDialog):
    def __init__(self):
        super(PomodoroUI,self).__init__()
        loadUi("./UI/pomodoro.ui",self)
        
        self.goToMainMenuButton.clicked.connect(self.go_main_menu)
        self.addTask.clicked.connect(self.add_task)
        


    
    def add_task(self):
        '''A handler function for the add recipient button click event.'''
        task = self.addTask.text()   # Get the recipient email the user entered
        # Check if it is already in the recipient list.
        print(MainMenuUI.current_subject, MainMenuUI.current_project)
        # print(MainMenuUI.current_subject2, MainMenuUI.current_project2)
        if task == "":
            self.errorTextRecipientsEmailLabel.setText("This field cannot be empty.")
            return
        else:
            # selected_index2 = self.projectDeleteCombo.currentIndex()
            # selected_index = self.subjectDeleteCombo.currentIndex()
            # Create a new Recipient from the email the user has entered and add it to recipients list and the recipients menu.
            task_name = Task(task)
            current_user.projects[0].subjects[0].PomodoroSessions[0].tasks.append(task_name)
            self.tasksCombo.addItem(task_name.name)
            self.tasksCombo.setCurrentIndex(len(task_name.name)-1)   # Select the new recipient in the menu (last one)
            save_data()

    
    def go_main_menu(self):
        main_menu = MainMenuUI()
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)
        


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