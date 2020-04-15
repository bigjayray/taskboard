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

            n_tasks = len(taskboard.tasks)
            n_ctasks = 0
            n_atasks = 0
            n_ctaskst = 0
            for i in taskboard.tasks:
                if i.completion == True:
                    n_ctasks += 1
                    today = datetime.date(datetime.now())
                    if datetime.date(i.completion_date) == today:
                        n_ctaskst += 1
                else:
                    n_atasks += 1

            user_key = ndb.Key('MyUser', user.user_id())
            myuser = user_key.get()

            permission = False

            taskboards_created_keys = myuser.taskboards_created
            for i in taskboards_created_keys:
                if i == taskboard.key:
                    permission = True

            # selection statement for user
            if user:

                q = MyUser.query().fetch()

                # values to be rendered to the createtaskboard.html page
                template_values = {
                    'user' : user,
                    'taskboard' : taskboard,
                    'permission' : permission,
                    'q' : q,
                    'n_tasks' : n_tasks,
                    'n_ctasks' : n_ctasks,
                    'n_atasks' : n_atasks,
                    'n_ctaskst' : n_ctaskst
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
        u_key = ndb.Key('MyUser', user.user_id())
        u = u_key.get()

        # get value of button clicked
        action = self.request.get('button')

        # selection statement for button
        if action == 'AddUser':

            # gets id passed in the form
            id = self.request.get('id')
            k_str = self.request.get('user_id')

            # gets TaskBoard
            taskboard = TaskBoard.get_by_id(int(id))
            taskboard_key = ndb.Key('TaskBoard', int(id))
            user_key = ndb.Key(urlsafe=k_str)
            myuser = user_key.get()

            for i in taskboard.users:
                if i == user_key:
                    self.redirect('/taskboards?id='+id)
                    return

            taskboard.users.append(user_key)
            myuser.taskboards.append(taskboard_key)

            taskboard.put()
            myuser.put()

            self.redirect('/taskboards?id='+id)

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

            for i in taskboard.tasks:
                if i.title == task.title:
                    self.redirect('/taskboards?id='+id)
                    return

            taskboard.tasks.append(task)

            taskboard.completion = False

            taskboard.put()

            self.redirect('/taskboards?id='+id)

        if action == 'Completed':

            # gets id passed in the form
            id = self.request.get('id')
            index = int(self.request.get('index'))

            time = datetime.now()

            # gets TaskBoard
            taskboard = TaskBoard.get_by_id(int(id))

            taskboard.tasks[index - 1].completion = True
            taskboard.tasks[index - 1].completion_date = time

            taskboard.put()


            self.redirect('/taskboards?id='+id)

        if action == 'Delete':

            # gets id passed in the form
            id = self.request.get('id')
            index = int(self.request.get('index'))

            # gets TaskBoard
            taskboard = TaskBoard.get_by_id(int(id))

            del taskboard.tasks[index - 1]

            taskboard.put()


            self.redirect('/taskboards?id='+id)

        if action == 'Edit':

            # gets id passed in the form
            id = self.request.get('id')
            index = int(self.request.get('index'))
            k_str = self.request.get('assigned_user')
            due_date = self.request.get('due_date')
            title = self.request.get('title')

            # gets TaskBoard
            taskboard = TaskBoard.get_by_id(int(id))

            # if taskboard.tasks[index - 1].title == title:
            #     self.redirect('/viewtaskboard')
            #     return

            taskboard.tasks[index - 1].title = title
            taskboard.tasks[index - 1].due_date = datetime.strptime(due_date, "%Y-%m-%d")
            taskboard.tasks[index - 1].assigned_user = ndb.Key(urlsafe=k_str)

            taskboard.put()


            self.redirect('/taskboards?id='+id)

        if action == 'Change':

            # gets id passed in the form
            id = self.request.get('id')

            # gets TaskBoard
            taskboard = TaskBoard.get_by_id(int(id))

            name = self.request.get('name')

            for i in u.taskboards:
                if i.get().name == name:
                    self.redirect('/taskboards?id='+id)
                    return

            taskboard.name = name

            taskboard.put()

            self.redirect('/taskboards?id='+id)

        if action == 'Drop':

            # gets id passed in the form
            id = self.request.get('id')
            k_str = self.request.get('assigned_user')

            # gets TaskBoard
            taskboard = TaskBoard.get_by_id(int(id))

            key = ndb.Key(urlsafe=k_str)
            index = 0
            for i in taskboard.users:
                if i == key:
                    del taskboard.users[index]
                index += 1

            for i in taskboard.tasks:
                if i.assigned_user == key:
                    i.assigned_user = None

            index = 0
            for i in key.get().taskboards:
                if i == taskboard.key:
                    del key.get().taskboards[index]
                index += 1

            taskboard.put()


            self.redirect('/taskboards?id='+id)

        if action == 'DeleteTaskboard':

            # gets id passed in the form
            id = self.request.get('id')

            # gets TaskBoard
            taskboard = TaskBoard.get_by_id(int(id))

            index = 0
            for i in u.taskboards:
                if i == taskboard.key:
                    del u.taskboards[index]
                index += 1

            u.put()
            taskboard.key.delete()


            self.redirect('/')


        elif action == 'Cancel':
            self.redirect('/')
