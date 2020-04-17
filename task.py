#imports
from google.appengine.ext import ndb

#Task class
class Task(ndb.Model):
    # A model for representing an task board
    #task attributes
    title = ndb.StringProperty(required=True)
    due_date = ndb.DateProperty(required=True)
    completion = ndb.BooleanProperty(default=False)
    completion_date = ndb.DateTimeProperty()
    assigned_user = ndb.KeyProperty(kind='MyUser')
