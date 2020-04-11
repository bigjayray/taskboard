from google.appengine.ext import ndb

class Task(ndb.Model):
    # A model for representing an task board
    title = ndb.StringProperty(required=True)
    due_date = ndb.DateProperty(required=True)
    completion = ndb.BooleanProperty(default=False)
    assigned_user = ndb.KeyProperty(kind='MyUser')
