import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from myuser import MyUser
from task import Task
from taskboard import TaskBoard

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class CreateTaskBoard(webapp2.RequestHandler):
    # get method called on page when page is instantiated
    def get(self):
        self.response.headers['Content-Typ'] = 'text/html'

        # gets current user
        user = users.get_current_user()

        # selection statement for user
        if user:

            # values to be rendered to the createtaskboard.html page
            template_values = {
                'user' : user,
            }

            template = JINJA_ENVIRONMENT.get_template('createtaskboard.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')

    # called when you submit a web form
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        # gets current user
        user = users.get_current_user()

        #generates user key
        user_key = ndb.Key('MyUser', user.user_id())

        # create a new taskboard object
        taskboard = TaskBoard()

        # get value of button clicked
        action = self.request.get('button')

        # selection statement for button
        if action == 'Create':

            taskboard.users.append(user_key)

            # adds form values to the ev object
            taskboard.name = self.request.get('name')

            taskboard.put()

            self.redirect('/')

        elif action == 'Cancel':
            self.redirect('/')
