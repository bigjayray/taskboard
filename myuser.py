from google.appengine.ext import ndb
from task import Task

class MyUser(ndb.Model):
    # email address of this user
    email_address = ndb.StringProperty()
    task_assigned = ndb.KeyProperty(kind=Task, repeated=True)
