from google.appengine.ext import ndb

from task import Task

class MyUser(ndb.Model):
    # email address of this user
    email_address = ndb.StringProperty()
    taskboards = ndb.KeyProperty(kind='TaskBoard', repeated=True)
    taskboards_created = ndb.KeyProperty(kind='TaskBoard', repeated=True)
    # task_assigned = ndb.KeyProperty(kind=Task, repeated=True)

class TaskBoard(ndb.Model):
    # A model for representing an task board
    name = ndb.StringProperty(required=True)
    users = ndb.KeyProperty(kind='MyUser', repeated=True)
    tasks = ndb.StructuredProperty(Task, repeated=True)

    # logic a user can have multi taskboards and a taskboard can have multiple users
