import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from myuser import MyUser
from task import Task
from myuser import TaskBoard
from datetime import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class TaskBoards(webapp2.RequestHandler):
    # get method called on page when page is instantiated
    def get(self):
        self.response.headers['Content-Typ'] = 'text/html'

        # gets current user
        user = users.get_current_user()

        # gets id passed in the url
        id = self.request.get('id')

        if id == '':

            self.redirect('/viewtaskboard')

        else:

            # gets TaskBoard
            taskboard = TaskBoard.get_by_id(int(id))

            user_key = ndb.Key('MyUser', user.user_id())
            myuser = user_key.get()

            permission = False

            taskboards_created_keys = myuser.taskboards_created
            for i in taskboards_created_keys:
                if i == taskboard.key:
                    permission = True

            # selection statement for user
            if user:

                # values to be rendered to the createtaskboard.html page
                template_values = {
                    'user' : user,
                    'taskboard' : taskboard,
                    'permission' : permission
                }

                template = JINJA_ENVIRONMENT.get_template('taskboards.html')
                self.response.write(template.render(template_values))
            else:
                self.redirect('/')

    # called when you submit a web form
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        # gets current user
        user = users.get_current_user()

        # get value of button clicked
        action = self.request.get('button')

        # selection statement for button
        if action == 'AddUser':

            # gets id passed in the form
            id = self.request.get('id')
            user_email = self.request.get('user_email')

            # gets TaskBoard
            taskboard = TaskBoard.get_by_id(int(id))
            taskboard_key = ndb.Key('TaskBoard', int(id))

            q = MyUser.query().filter(MyUser.email_address == user_email)

            if q.count() == 0:
                error = True

                template_values = {
                    'user' : user,
                    'taskboard' : taskboard,
                    'error' : error
                }

                template = JINJA_ENVIRONMENT.get_template('taskboards.html')
                self.response.write(template.render(template_values))
            else:

                for i in q.iter(keys_only=True):
                    user_key = i

                taskboard.users.append(user_key)

                myuser = user_key.get()
                myuser.taskboards.append(taskboard_key)

                taskboard.put()
                myuser.put()

                template_values = {
                    'user' : user,
                    'taskboard' : taskboard
                }

                template = JINJA_ENVIRONMENT.get_template('taskboards.html')
                self.response.write(template.render(template_values))

        if action == 'AddTask':
            #create a new task
            task = Task()

            # gets id passed in the form
            id = self.request.get('id')

            #add form values to task
            task.title = self.request.get('title')
            k_str = self.request.get('assigned_user')
            task.assigned_user = ndb.Key(urlsafe=k_str)
            due_date = self.request.get('due_date')

            task.due_date = datetime.strptime(due_date, "%Y-%m-%d")

            # gets TaskBoard
            taskboard = TaskBoard.get_by_id(int(id))

            taskboard.tasks.append(task)

            taskboard.completion = False

            taskboard.put()

            # values to be rendered to the createtaskboard.html page
            template_values = {
                'user' : user,
                'taskboard' : taskboard
            }

            template = JINJA_ENVIRONMENT.get_template('taskboards.html')
            self.response.write(template.render(template_values))

        if action == 'AssignTask':

            # gets TaskBoard
            taskboard = TaskBoard.get_by_id(int(id))

            # values to be rendered to the createtaskboard.html page
            template_values = {
            'user' : user,
            'taskboard' : taskboard
            }

            template = JINJA_ENVIRONMENT.get_template('taskboards.html')
            self.response.write(template.render(template_values))

        #
        # elif action == 'Cancel':
        #     self.redirect('/')
