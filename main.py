#imports
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from myuser import MyUser
from createtaskboard import CreateTaskBoard
from myuser import TaskBoard
from taskboards import TaskBoards
from viewtaskboard import ViewTaskBoard


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

#MainPage class
class MainPage(webapp2.RequestHandler):
    #get method called by webapp2 in response to HTTP get request
    def get(self):
        self.response.headers['Content-Typ'] = 'text/html'

        #initializing variables
        url = ''
        url_string = ''
        welcome = 'Welcome back'
        myuser = None

        #gets current user
        user = users.get_current_user()

        #selection for user
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

            #gets user key
            myuser_key = ndb.Key('MyUser', user.user_id())

            #generates user from key
            myuser = myuser_key.get()

            if myuser == None:
                welcome = 'Welcome to the application'
                myuser = MyUser(id=user.user_id())
                #adds mail attribute
                myuser.email_address = user.email()
                #saves user to datastore
                myuser.put()
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        #assign template values to be rendered to the html page
        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome' : welcome,
            'myuser' : myuser
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


# specify the full routing table 
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/createtaskboard', CreateTaskBoard),
    ('/taskboards', TaskBoards),
    ('/viewtaskboard', ViewTaskBoard)
], debug=True)
