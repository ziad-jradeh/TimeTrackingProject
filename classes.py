import datetime
import json

class User():
    '''User class (name: String, email: String, **attributes: Dictionary)
    
    This class holds the data for each User.'''
    
    def __init__(self, name, email, **attr):
        self.name = name
        self.email = email
        self.projects = []
        self.recipients = []
        
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
        self.PomodoroSessions = []
        self.__dict__.update(attr)
    

class PomodoroSession():
    '''PomodoroSession class (name: String, **attributes: Dictionary)
    
    This class holds the data for each PomodoroSession.'''
    
    def __init__(self, number):
        self.number = number
        
        # Temporary values, to be fixed later
        self.starting_time = datetime.datetime.now()
        self.end_time = datetime.datetime.now()
        self.date = datetime.datetime.now()
        
        self.tasks = []


class Task():
    def __init__(self, name):
        self.name = name
        self.finished = False


class Recipient():
    def __init__(self, email, **attr):
        self.email = email
        self.__dict__.update(attr)
        
    def send_summary(summary):
        pass


class JsonEncoder(json.JSONEncoder):
    '''This class implements a JSON encoder to encode the given object to json.'''
    def default(self, obj):
        return obj.__dict__  


def dict_to_user(user_dict):
    '''A function to convert a dictionary to a User object. Returns a User object.'''
    
    # Create a User object from the user dictionary that contains all its attributes and data.
    user = User(**user_dict)
    
    # Create the Projects and Subjects inside the User object from their dictionaries.
    for i, project_dict in enumerate(user.projects):
        user.projects[i] = Project(**project_dict)
        for j, subject_dict in enumerate(user.projects[i].subjects):
            user.projects[i].subjects[j] = Subject(**subject_dict)
    
    # Create the Recipients inside the User object from their dictionaries.
    for i, recipient_dict in enumerate(user.recipients):
        user.recipients[i] = Recipient(**recipient_dict)
        
    # Return the full User object with all it's data.
    return user

