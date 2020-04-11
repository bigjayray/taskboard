import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from myuser import MyUser
from myuser import TaskBoard


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class ViewTaskBoard(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Typ'] = 'text/html'

        user = users.get_current_user()
        user_key = ndb.Key('MyUser', user.user_id())
        myuser = user_key.get()

        taskboards_keys = myuser.taskboards

        taskboards = ndb.get_multi(taskboards_keys)

        template_values = {
            'user' : user,
            'taskboards' : taskboards
        }

        template = JINJA_ENVIRONMENT.get_template('viewtaskboard.html')
        self.response.write(template.render(template_values))
