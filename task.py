from google.appengine.ext import ndb

class Task(ndb.Model):
    # A model for representing an task board
    activity = ndb.StringProperty(required=True)
    create_date = ndb.DateTimeProperty(auto_now=True)
