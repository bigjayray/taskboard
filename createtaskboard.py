import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from myuser import MyUser
from task import Task
from myuser import TaskBoard

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class CreateTaskBoard(webapp2.RequestHandler):
    # get method called by webapp2 when page is instantiated
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
            #if no logged in user redirect to home page
            self.redirect('/')

    # called when form is submitted on createtaskboard.html page
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        # gets current user
        user = users.get_current_user()

        #generates user key
        user_key = ndb.Key('MyUser', user.user_id())

        #generates user
        myuser = user_key.get()

        # create a new taskboard object
        taskboard = TaskBoard()
        #do you want us to implement parent child relationship like taskboard = TaskBoard(parent=user_key)
        #had errors retrieving taskboard keys implementing that

        # get value of button clicked
        action = self.request.get('button')

        # selection statement for button
        if action == 'Create':

            # gets taskboard name from form
            name = self.request.get('name')

            # loops through all taskboards created by user and added by user
            for i in myuser.taskboards:
                # if taskboard found with same name display error message
                if i.get().name == name:

                    error = True
                    # values to be rendered to the createtaskboard.html page
                    template_values = {
                        'user' : user,
                        'error' : error
                    }

                    template = JINJA_ENVIRONMENT.get_template('createtaskboard.html')
                    self.response.write(template.render(template_values))
                    return

            # add form values to taskboard attributes
            taskboard.users.append(user_key)
            taskboard.name = name
            taskboard.creator = user_key

            # saves taskboard to datastore
            taskboard.put()

            # add taskboard to user attributes
            myuser.taskboards.append(taskboard.key)
            myuser.taskboards_created.append(taskboard.key)

            #saves updated user object
            myuser.put()

            #redirects user to the page with all taskboards listed
            self.redirect('/viewtaskboard')
