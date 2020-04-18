#imports
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

#ViewTaskBoard class
class ViewTaskBoard(webapp2.RequestHandler):
    #get method called by webapp2 in response to HTTP get request
    def get(self):
        self.response.headers['Content-Typ'] = 'text/html'

        #gets current user
        user = users.get_current_user()

        # selection statement for user
        if user:
            #gets user key
            user_key = ndb.Key('MyUser', user.user_id())
            #gets user
            myuser = user_key.get()

            #gets all taskboard keys in user
            taskboards_keys = myuser.taskboards
            #gets all taskboards
            taskboards = ndb.get_multi(taskboards_keys)

            #if user has no taskboard redirect to createtaskboard
            if taskboards == []:
                self.redirect('/createtaskboard')

            #assign template values to be rendered to the html page
            template_values = {
                'user' : user,
                'taskboards' : taskboards
            }

            template = JINJA_ENVIRONMENT.get_template('viewtaskboard.html')
            self.response.write(template.render(template_values))
        else:
            #if no user redirect back to home page
            self.redirect('/')
