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
    
    def __init__(self, name):
        self.name = name
        self.subjects = []
    
    
        
        
    
    

class Subject():
    '''Subject class (name: String, **attributes: Dictionary)
    
    This class holds the data for each subject.'''
    
    def __init__(self, name, **attr):
        self.name = name
        self.PomodoroSessions = []
        self.__dict__.update(attr)
    
   
    

class PomodoroSessions():
    '''PomodoroSession class (name: String, **attributes: Dictionary)
    
    This class holds the data for each PomodoroSession.'''
    
    def __init__(self, number):
        self.number = number
        
        # Temporary values, to be fixed later
        self.starting_time = str(datetime.datetime.now())
        # self.end_time = datetime.datetime.now()
        # self.date = datetime.datetime.now()
        
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

        
        

class Struct(object):
    def __init__(self, data):
        for name, value in data.items():
            setattr(self, name, self._wrap(value))

    def _wrap(self, value):
        if isinstance(value, (tuple, list, set, frozenset)): 
            return type(value)([self._wrap(v) for v in value])
        else:
            return Struct(value) if isinstance(value, dict) else value
