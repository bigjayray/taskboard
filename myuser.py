#imports
from google.appengine.ext import ndb
from task import Task

#MyUser class
class MyUser(ndb.Model):
    # A model for representing a user
    #user attributes
    email_address = ndb.StringProperty()
    taskboards = ndb.KeyProperty(kind='TaskBoard', repeated=True)
    taskboards_created = ndb.KeyProperty(kind='TaskBoard', repeated=True)
    # task_assigned = ndb.KeyProperty(kind=Task, repeated=True)

#TaskBoard class
class TaskBoard(ndb.Model):
    # A model for representing an task board
    # taskboard attributes
    name = ndb.StringProperty(required=True)
    users = ndb.KeyProperty(kind='MyUser', repeated=True)
    tasks = ndb.StructuredProperty(Task, repeated=True)
    creator = ndb.KeyProperty(kind='MyUser')

    # logic a user can have multi taskboards and a taskboard can have multiple users
