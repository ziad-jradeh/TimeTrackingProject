import json
from PyQt5.QtCore import QDateTime, QTime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

date_time_format = "dd-MM-yyyy HH:mm:ss"
time_format = "HH:mm:ss"
date_format = "dd-MM-yyyy"

class User():
    '''User class (name: String, email: String, **attributes: Dictionary)
    
    This class holds the data for each User.'''
    
    def __init__(self, name, email, **attr):
        self.name = name
        self.email = email
        self.projects = []
        self.recipients = []
        self.total_tracked_time = QTime(0, 0, 0).toString(time_format)
        
        # Load the attributes from a dictionary that contains all the attributes
        self.__dict__.update(attr)
    

class Project():
    '''Project class (name: String, **attributes: Dictionary)
    
    This class holds the data for each Project.'''
    
    def __init__(self, name, **attr):
        self.name = name
        self.subjects = []
        
        # Load the attributes from a dictionary that contains all the attributes
        self.__dict__.update(attr)
    
    

class Subject():
    '''Subject class (name: String, **attributes: Dictionary)
    
    This class holds the data for each subject.'''
    
    def __init__(self, name, **attr):
        self.name = name
        self.pomodoros = []
        
        # Load the attributes from a dictionary that contains all the attributes
        self.__dict__.update(attr)

    
class Pomodoro():
    def __init__(self, **attr):
        # Unique identifier based on the seconds since the epoch
        self.UID = QDateTime.currentSecsSinceEpoch()
        
        self.pomodoro_sessions = []
        
        self.__dict__.update(attr)
    
    
    
    ### SIMPLIFY THIS STARTING TIME OF FIRST SESSION TO END TIME OF THE LAST SESSION
    @property
    def starting_time(self):
        '''A property for the starting time of the Pomodoro.'''
        if len(self.pomodoro_sessions) == 0:
            return None
        else:
            datetime = QDateTime.fromString(self.pomodoro_sessions[0].starting_time, date_time_format)
            time = datetime.time()
            return time
    
    @property
    def end_time(self):
        '''A property for the end time of the Pomodoro.'''
        if len(self.pomodoro_sessions) == 0:
            return None
        else:
            datetime = QDateTime.fromString(self.pomodoro_sessions[0].end_time, date_time_format)
            time = datetime.time()
            return time
    
    @property
    def date(self):
        '''A property for the date of the Pomodoro.'''
        if len(self.pomodoro_sessions) == 0:
            return None
        else:
            datetime = QDateTime.fromString(self.pomodoro_sessions[0].starting_time, date_time_format)
            date = datetime.date()
            return date
        
class PomodoroSession():
    '''PomodoroSession class (name: String, **attributes: Dictionary)
    
    This class holds the data for each PomodoroSession.'''
    
    def __init__(self, number, **attr):
        # Unique identifier based on the seconds since the epoch
        self.UID = QDateTime.currentSecsSinceEpoch()
        self.number = number
        
        self.starting_time = None
        self.end_time = None
        self.date = None
        
        self.tasks = []
        
        self.__dict__.update(attr)

    def get_summary(self, new_line = '\n'):
        finished_tasks = ""
        unfinished_tasks = ""
        for task in self.tasks:
            if task.finished:
                finished_tasks += task.name + new_line
            else:
                unfinished_tasks += task.name + new_line
        s_time = QDateTime.fromString(self.starting_time, date_time_format).time().toString(time_format)
        e_time = QDateTime.fromString(self.end_time, date_time_format).time().toString(time_format)
        date = QDateTime.fromString(self.date, date_time_format).date().toString("dd/MM/yyyy")
        return [date, s_time, e_time, finished_tasks, unfinished_tasks]

class Task():
    '''Task class (name: String, **attributes: Dictionary)
    
    This class holds the data for each Task.'''
    
    def __init__(self, name, **attr):
        self.name = name
        self.finished = False

        self.__dict__.update(attr)


class Recipient():
    '''Recipient class (email: String, **attributes: Dictionary)
    
    This class holds the data for each Recipient.'''
    
    def __init__(self, email, **attr):
        self.email = email
        
        self.__dict__.update(attr)
        
    def send_summary(self, html_data):
        '''A function to send a summary to the recipient.'''
       
        
        to_address = self.email
        
        message = MIMEMultipart()
        message['From'] = 'selampomodoro@gmail.com'
        message['To'] = to_address
        message['Subject'] = 'Pomodoro Session Data'
        
        # message body
        body = MIMEText(html_data, 'html')
        message.attach(body)

        # create  SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # login
        email = 'selampomodoro@gmail.com'
        password = 'kdgwbgjveajwjxvl'
        server.login(email, password)

        server.sendmail(email, to_address, message.as_string())
        server.quit()

class Break():
    '''An abstract class for breaks.'''
    def __init__(self, period):
        self.period = period
        self.starting_time = None
        self.end_time = None
        
class ShortBreak(Break):
    '''Short break class inhereted from the abstract Break class. It's default period is 5 minutes'''
    def __init__(self, period = 5):
        super().__init__(period)
        
class LongBreak(Break):
    '''Long break class inhereted from the abstract Break class. It's default period is 30 minutes'''
    def __init__(self, period = 30):
        super().__init__(period)
        
    
class JsonEncoder(json.JSONEncoder):
    '''This class implements a JSON encoder to encode the given object to json.'''
    def default(self, obj):
        return obj.__dict__  


def dict_to_user(user_dict):
    '''A function to convert a dictionary to a User object. Returns a User object.'''
    
    # Create a User object from the user dictionary that contains all its attributes and data.
    user = User(**user_dict)
    
    # Create the Projects and Subjects and other objects inside the User object from their dictionaries.
    for i, project_dict in enumerate(user.projects):
        user.projects[i] = Project(**project_dict)
        for j, subject_dict in enumerate(user.projects[i].subjects):
            user.projects[i].subjects[j] = Subject(**subject_dict)
            for k, pomodoro_dict in enumerate(user.projects[i].subjects[j].pomodoros):
                user.projects[i].subjects[j].pomodoros[k] = Pomodoro(**pomodoro_dict)
                for l, session_dict in enumerate(user.projects[i].subjects[j].pomodoros[k].pomodoro_sessions):
                    user.projects[i].subjects[j].pomodoros[k].pomodoro_sessions[l] = PomodoroSession(**session_dict)
                    for m, task_dict in enumerate(user.projects[i].subjects[j].pomodoros[k].pomodoro_sessions[l].tasks):
                        user.projects[i].subjects[j].pomodoros[k].pomodoro_sessions[l].tasks[m] = Task(**task_dict)
    
    # Create the Recipients inside the User object from their dictionaries.
    for i, recipient_dict in enumerate(user.recipients):
        user.recipients[i] = Recipient(**recipient_dict)
        
    # Return the full User object with all it's data.
    return user
