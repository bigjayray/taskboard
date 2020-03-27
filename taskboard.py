from google.appengine.ext import ndb
from myuser import MyUser
from task import Task

class TaskBoard(ndb.Model):
    # A model for representing an task board
    users = ndb.StructuredProperty(MyUser, repeated=True)
    tasks = ndb.StructuredProperty(Task, repeated=True)
