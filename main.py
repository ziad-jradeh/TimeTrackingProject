from time import time
from PyQt5 import QtWidgets
import PyQt5
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem
from PyQt5.uic import loadUi
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QDateTime, QTime, QDate


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
        users_list = {user_dict["email"]: dict_to_user(user_dict) for user_dict in json_data.values()}
        
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
        
        if name == '' or email == '':
            self.errorTextSignUp.setText("Name and email cannot be empty.")
        elif users_list.get(email) is not None:
            self.errorTextSignUp.setText("Email already registered. please log in.")
        else:
            # if the email is not found in the users list, create a new account.
            user = User(name, email)
            # add the account to the users list
            users_list[email] = user
            self.errorTextSignUp.setText("Account created for " + user.email + " You can now login")
        
        # Write the new users list to the json data file.
        save_data()
        
 
    def login(self):
        '''A handler function for the login button click event.'''
        
        email = self.emailInputLogin.text()     # read the email the user entered
        try:
            global current_user
            current_user = users_list[email]
            self.go_main_menu()
        except KeyError:
            # if the email was not found, show an error message.
            self.errorTextLogin.setText(f"No account for {email}, please sign up first.")


    def go_main_menu(self):
        main_menu = MainMenuUI()
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)


class MainMenuUI(QDialog):
    
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
        self.showSummaryButton.clicked.connect(self.show_summary)
        self.sendEmailThisSummaryButton.clicked.connect(self.send_summary)

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
        
        self.titleWorkspaceLabel.setText(f"{current_user.name}'s workspace")
        self.recipientTitleLabel.setText(f"{current_user.name}'s recipients")
        
        self.projectDeleteCombo.activated.connect(self.check_index2)
        # self.addSubjectOnProjectCombo.activated.connect(self.check_index)
        
        
        self.subjectDeleteCombo.clear()
        if  len(current_user.projects) > 0:
            self.subjectDeleteCombo.addItems([subject.name for subject in current_user.projects[selected_index].subjects])
        
        self.errorTextRecipientsEmailLabel.clear()
        self.errorTextProjectLabel.clear()
        self.errorTextSubjectLabel.clear()
        self.showSummarySubjectCombo.clear()
        self.showSummarySubjectCombo.addItem("All")
        
        self.showSummaryProjectCombo.clear()
        self.showSummaryProjectCombo.addItem("All")
        self.showSummaryProjectCombo.addItems([project.name for project in current_user.projects])
        self.showSummaryProjectCombo.activated.connect(self.check_index3)
        
        self.totalTrackedTimeDurationLabel.setText(current_user.total_tracked_time)
        self.show_summary()
        

    def check_index(self, index):
        self.selectSubjectCombo.clear()
        self.selectSubjectCombo.addItems([subject.name for subject in current_user.projects[index].subjects])
        
    def check_index2(self, index):
        self.subjectDeleteCombo.clear()
        self.subjectDeleteCombo.addItems([subject.name for subject in current_user.projects[index].subjects])
        
    def check_index3(self, index):
        if index <= 0:
            self.showSummarySubjectCombo.clear()
            self.showSummarySubjectCombo.addItem("All")
        else:
            self.showSummarySubjectCombo.clear()
            self.showSummarySubjectCombo.addItem("All")
            self.showSummarySubjectCombo.addItems([subject.name for subject in current_user.projects[index-1].subjects])
        
        

    
        
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
            current_user.recipients.append(recipient) # recipient is added to the current_user.recipients lis
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
        project_name = self.addProjectInput.text()
        if project_name == "":
            self.errorTextProjectLabel.setText("This field cannot be empty.")
            return
        elif project_name in [i.name for i in current_user.projects]:
            self.errorTextProjectLabel.setText(f"{project} is already in the recipients list.")
        else:
            project = Project(project_name)
            MainMenuUI.current_project2 = project_name

            current_user.projects.append(project)
            self.projectDeleteCombo.addItem(project.name)
            self.projectDeleteCombo.setCurrentIndex(len(current_user.projects)-1)   # Select the new recipient in the menu (last one)
            self.addSubjectOnProjectCombo.addItem(project.name)
            self.addSubjectOnProjectCombo.setCurrentIndex(len(current_user.projects)-1)   # Select the new recipient in the menu (last one)
            self.selectProjectCombo.addItem(project.name)
            self.selectProjectCombo.setCurrentIndex(len(current_user.projects)-1)   # Select the new recipient in the menu (last one)
            self.errorTextProjectLabel.setText(f"{project_name} has been added.")
            self.showSummaryProjectCombo.clear()
            self.showSummaryProjectCombo.addItem("All")
            self.showSummaryProjectCombo.addItems([pro.name for pro in current_user.projects])
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
    
    def show_summary(self):
        self.totalTrackedTimeDurationLabel.setText(current_user.total_tracked_time)
        project_index = self.showSummaryProjectCombo.currentIndex()
        subject_index = self.showSummarySubjectCombo.currentIndex()
        data = []
        if project_index == 0:
            for project in current_user.projects:
                for subject in project.subjects:
                    for pomodoro in subject.pomodoros:
                        for pomodoro_session in pomodoro.pomodoro_sessions:
                            data.append(pomodoro_session)
        elif subject_index == 0:
            for subject in current_user.projects[project_index-1].subjects:
                for pomodoro in subject.pomodoros:
                    for pomodoro_session in pomodoro.pomodoro_sessions:
                        data.append(pomodoro_session)      
        else:
            for pomodoro in current_user.projects[project_index-1].subjects[subject_index-1].pomodoros:
                for pomodoro_session in pomodoro.pomodoro_sessions:
                    data.append(pomodoro_session)
            #data = [session.get_summary() for session in current_user.projects[project_index-1].subjects[subject_index-1].pomodoros[0].pomodoro_sessions]
        global period_text
        period_text = self.showSummaryPeriodCombo.currentText()
        
        end = QDateTime.currentDateTime()
        start = QDateTime.currentDateTime()
        
        
        filtered_sessions = []
        
        if period_text == 'All':
            filtered_sessions = data
        elif period_text == 'Today':
            start.setTime(QTime(0, 0, 0))
            for session in data:
                session_start = QDateTime.fromString(session.starting_time, date_time_format)
                if end >= session_start >= start:
                    filtered_sessions.append(session)
        elif period_text == "This week":
            start = start.addDays(-7)
            for session in data:
                session_start = QDateTime.fromString(session.starting_time, date_time_format)
                if end >= session_start >= start:
                    filtered_sessions.append(session)
        elif period_text == "This month":
            start = start.addDays(-30)
            for session in data:
                session_start = QDateTime.fromString(session.starting_time, date_time_format)
                if end >= session_start >= start:
                    filtered_sessions.append(session)
        
        summary = [session.get_summary() for session in filtered_sessions]
        
        self.summaryTableValuesWidget.setRowCount(len(summary))  # set the number of rows in the table
        for row in range(len(summary)):
            for col in range(5):
                item = QTableWidgetItem(str(summary[row][col]))  # create a QTableWidgetItem for each cell
                self.summaryTableValuesWidget.setItem(row, col, item)  # add the item to the table
        global summary_html
        summary_html = [session.get_summary("<br>") for session in filtered_sessions]
        
    
    def send_summary(self):
         # html table 
        html_data = '''<head>
                    <style>
                    table {
                    font-family: arial, sans-serif;
                    border-collapse: collapse;
                    width: 100%;
                    }

                    td, th {
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                    }

                    tr:nth-child(even) {
                    background-color: #dddddd;
                    }
                    </style>
                    </head>'''
        table_html = '<table><tr><th>Date</th><th>Starting Time</th><th>End Time</th><th>Success(Tasks)</th><th>Failure(Tasks)</th></tr>'
        for row in summary_html:
            table_html += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(*row)  
        table_html += '</table>'
        
        html_data += f'<h1>Pomodoro Data of {current_user.name} for {period_text}:</h1><br><h2>Total Tracked Time: {current_user.total_tracked_time}</h2><br>{table_html}'
        
        
        # current_user.recipients[0].send_summary(html_data)
        for recipient in current_user.recipients:
            recipient.send_summary(html_data)


   


    def go_pomodro(self):

        index1 = self.selectProjectCombo.currentIndex()
        index2 = self.selectSubjectCombo.currentIndex()
        global current_subject, current_project
        current_subject = current_user.projects[index1].subjects[index2]
        current_project = current_user.projects[index1]
        save_data()
        
        Pomodoro_Session = PomodoroUI()
        widget.addWidget(Pomodoro_Session)
        widget.setCurrentIndex(widget.count()-1)
        # print(MainMenuUI.current_project,MainMenuUI.current_subject)
        
        
class PomodoroUI(QDialog):
    pomodoro_session_counter = 0
    def __init__(self):
        super(PomodoroUI,self).__init__()
        loadUi("./UI/pomodoro.ui",self)
        
        # Define the selected project, subject, pomodoro and session as global objects
        global current_project, current_subject, current_pomodoro, current_pomodoro_session
        
        # Create a new Pomodoro and add it to the list
        current_pomodoro = Pomodoro()
        current_subject.pomodoros.append(current_pomodoro)
        
        # Set up event handlers
        self.addTask.clicked.connect(self.add_task)
        self.tasksCombo.currentIndexChanged.connect(self.select_task)
        self.labelAsNotFinishedButton.clicked.connect(self.change_task_status)
        self.startStopButton.clicked.connect(self.start_pause_session)
        self.doneButton.clicked.connect(self.end_session)
        self.tasksCombo_2.currentIndexChanged.connect(self.update_task_status_button)
        self.goToMainMenuButton.clicked.connect(self.goToMainMenu)
        

        
        self.setup_session()
    
    def setup_session(self):
        '''A function to setup a new session and resets the PomodoroUI components.'''
        # Create a new PomodoroSession and increase their count in the current pomodoro UI
        global current_pomodoro_session
        current_pomodoro_session = PomodoroSession(self.pomodoro_session_counter)
        self.pomodoro_session_counter += 1
        self.numberOfSession.setText(str(self.pomodoro_session_counter))
        self.taskInput.setText("")
        self.startStopButton.setText("Start")
        self.tasksCombo.clear()
        self.tasksCombo_2.clear()
        self.update_task_status_button()
        
        # Create a new timer and time objects to be used for the countdown
        self.timer = QTimer()
        self.time = QTime(0, 25, 0) 
        self.timer.timeout.connect(self.show_time)
        
        
    def add_task(self):
        task_name = self.taskInput.text()   # get the task name the user has entered
        if task_name == "":                 # if it's empyt, exit the function
            return
        
        # If the task name is not empty, create a new task and add it to the tasks list and combos
        task = Task(task_name)
        current_pomodoro_session.tasks.append(task)
        self.tasksCombo.addItem(task.name)
        self.tasksCombo.setCurrentIndex(self.tasksCombo.count()-1)
        self.tasksCombo_2.addItem(task.name)
        
        # the start, label as finished, and done buttons are enabled only after a task is added
        self.startStopButton.setEnabled(True)
        self.labelAsNotFinishedButton.setEnabled(True)
        self.doneButton.setEnabled(True)
        save_data()
        
    def select_task(self, index):
        # When the user selects a task from the tasks combo box, the current_task object is assigned to the selected task.
        if index < 0: return
        global current_task
        current_task = current_pomodoro_session.tasks[index]
    
    def update_task_status_button(self):
        # Handle the finished / not finished button text when a task is selected from the tasks combo box.
        index = self.tasksCombo_2.currentIndex()
        if index < 0: return
        if current_pomodoro_session.tasks[index].finished:
            self.labelAsNotFinishedButton.setText("Label as not finished")
        else:
            self.labelAsNotFinishedButton.setText("Label as finished")
    
        
    def change_task_status(self):
        '''A fuction that flips the status of the current task.'''
        index = self.tasksCombo_2.currentIndex()
        current_pomodoro_session.tasks[index].finished = not current_pomodoro_session.tasks[index].finished
        save_data()
        self.update_task_status_button()
        
        
    def show_time(self):
        # Check if the timer has reached 00:00:00 and end the session if so.
        if self.time == QTime(0, 0, 0):
            self.end_session()
            return
        # If the timer has not reached 00:00:00, subtract a second and display the new time.
        self.time = self.time.addSecs(-1)
        self.timeLabel.setText(self.time.toString("mm:ss"))
        
        # add a second to the total tracked time of the user
        current_user.total_tracked_time = QTime.fromString(current_user.total_tracked_time, time_format).addSecs(1).toString(time_format)
        save_data()
        
    def start_pause_session(self):
        # if no task is selected, exit immediately
        if self.tasksCombo.currentIndex() == -1:
            return
        # if the timer is active, pause it and update the button text
        if self.timer.isActive():
            self.timer.stop()
            self.startStopButton.setText("Start")
        else:       # if the timer is not active, start it and update the button text
            self.timer.start(1000)
            self.startStopButton.setText("Pause")
            # if this is the first time the timer is started for this session,
            # update the starting time and date of the session
            if current_pomodoro_session.starting_time is None:
                current_pomodoro_session.starting_time = QDateTime.currentDateTime().toString(date_time_format)
                current_pomodoro_session.date = QDateTime.currentDateTime().toString(date_time_format)
        
        save_data()
    
    def end_session(self):
        # Stop the timer and save the end time of the session
        self.timer.stop()
        current_pomodoro_session.end_time = QDateTime.currentDateTime().toString(date_time_format)
        
        # Show a message box asking the user if the selected task is finished
        qm = QtWidgets.QMessageBox()
        ret = qm.question(self,'', f"Is task {current_task.name} finished?", qm.Yes | qm.No)
        if ret == qm.Yes:
            current_task.finished = True
        else:
            current_task.finished = False
        
        # add the session to the sessions list
        current_pomodoro.pomodoro_sessions.append(current_pomodoro_session)
        save_data()
        
        # Logic for deciding if the next break is long or short
        if self.pomodoro_session_counter < 4:       # Short Break
            self.setup_session()            # setup for the next session
            self.time = QTime(0, 25, 0)     # reset the timer
            self.timeLabel.setText(self.time.toString("mm:ss"))
            # go to shortBreakUI
            shortBreakUI = ShortBreakUI()
            widget.addWidget(shortBreakUI)
            widget.setCurrentIndex(widget.count()-1)
        else:                               # Long Break
            # go to longBreakUI
            longBreakUI = LongBreakUI()
            widget.addWidget(longBreakUI)
            widget.setCurrentIndex(widget.count()-1)
    
    

        
    def goToMainMenu(self):
        save_data()
        widget.setCurrentIndex(1)

class ShortBreakUI(QDialog):
    def __init__(self):
        super(ShortBreakUI,self).__init__()
        loadUi("./UI/shortBreak.ui",self)
        
        # Setup the event handlers
        self.startButton.clicked.connect(self.startTimer)
        self.skipButton.clicked.connect(self.stopTimer)
        self.goToMainMenuButton.clicked.connect(self.goToMainMenu)
        
        global short_break
        short_break = ShortBreak(5)
        
        # Create a new timer and time variables for the countdown
        self.timer = QTimer()
        self.time = QTime(0, 5, 0)
        self.timer.timeout.connect(self.show_time)
    
    
    def show_time(self):
        # if the timer reaches 00:00:00, stop it and go to Pomodoro UI
        if self.time == QTime(0, 0, 0):
            self.stopTimer()
            return
        # if the timer has not reached 00:00:00, subtract 1 second from time
        self.time = self.time.addSecs(-1)
        self.timeLabel.setText(self.time.toString("mm:ss"))
        
    def startTimer(self):
        if self.timer.isActive():       # if the timer is already running, pause it
            self.timer.stop()
            self.startButton.setText("Start")
        else:                           # if the timer not already running, start it
            self.timer.start(1000)
            self.startButton.setText("Pause")
    
    def stopTimer(self):
        self.timer.stop()
        widget.setCurrentIndex(2)
        
    def goToMainMenu(self):
        self.timer.stop()
        save_data()
        widget.setCurrentIndex(1)

class LongBreakUI(QDialog):
    def __init__(self):
        super(LongBreakUI,self).__init__()
        loadUi("./UI/longBreak.ui",self)
        
        # Setup the event handlers
        self.startButton.clicked.connect(self.startTimer)
        self.goToMainMenuButton.clicked.connect(self.stopTimer)
        self.skipButton.clicked.connect(self.stopTimer)
        
        global long_break
        long_break = ShortBreak(30)
        
        # Create a new timer and time variables for the countdown
        self.timer = QTimer()
        self.time = QTime(0, 30, 0)
        self.timer.timeout.connect(self.show_time)
    
    
    def show_time(self):
        # if the timer reaches 00:00:00, stop it and go to main menu UI
        if self.time == QTime(0, 0, 0):
            self.stopTimer()
            return
        # if the timer has not reached 00:00:00, subtract 1 second from time
        self.time = self.time.addSecs(-1)
        self.timeLabel.setText(self.time.toString("mm:ss"))
        
    def startTimer(self):
        if self.timer.isActive():       # if the timer is already running, pause it
            self.timer.stop()
            self.startButton.setText("Start")
        else:                           # if the timer not already running, start it
            self.timer.start(1000)
            self.startButton.setText("Pause")
    
    def stopTimer(self):
        self.timer.stop()
        save_data()
        widget.setCurrentIndex(1)

def save_data():
    '''A function that saves the data for all the users in a json file.
    Also creates a backup copy before.'''
    # backup the data file, in case the used file becomes corrupted.
    # shutil.copyfile(data_file, backup_file)
    
    # Convert the users list to dictionaries and save it to the json data file.
    with open(data_file, 'w') as f:
        json.dump(users_list, f, indent=4, cls= JsonEncoder)


app = QApplication(sys.argv)
UI = LoginUI() # This line determines which screen you will load at first


widget = QtWidgets.QStackedWidget()
widget.addWidget(UI)
widget.setFixedWidth(800)
widget.setFixedHeight(600)
widget.setWindowTitle("Time Tracking App")
widget.show()
sys.exit(app.exec_())
