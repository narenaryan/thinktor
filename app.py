#For tornado server stuff 

import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.websocket
import tornado.httpserver
from tornado.concurrent import Future


from jinja2 import Environment, FileSystemLoader #For templating stuff

import rethinkdb as r #For db stuff

from rethinkdb.errors import RqlRuntimeError, RqlDriverError

from conf import * #Fetching db and table details here


#Load the template environment
template_env = Environment(loader=FileSystemLoader("templates"))

db_connection = r.connect(RDB_HOST,RDB_PORT) #Connecting to RethinkDB server

subscribers = set() 


def dbSetup():
    print PROJECT_DB,db_connection
    try:
        r.db_create(PROJECT_DB).run(db_connection)
        print 'Database setup completed.'
    except RqlRuntimeError:
        try:
            r.db(PROJECT_DB).table_create(PROJECT_TABLE).run(db_connection)
            print 'Table creation completed'
        except:
            print 'Table already exists.Nothing to do'
        print 'App database already exists.Nothing to do'

    db_connection.close()

r.set_loop_type("tornado")


class MainHandler(tornado.web.RequestHandler): #Class that renders login page
    @tornado.gen.coroutine
    def get(self):
        detail_template = template_env.get_template("detail.html") #Loads tenplate
        self.write(detail_template.render())
    
    @tornado.gen.coroutine
    def post(self):
        home_template = template_env.get_template("home.html")
        email = self.get_argument("email")
        name = self.get_argument("nickname")
        connection = r.connect(RDB_HOST, RDB_PORT, PROJECT_DB)
        #Thread the connection
        threaded_conn = yield connection
        result = r.table(PROJECT_TABLE).insert({ "name": name , "email" : email}, conflict="error").run(threaded_conn)
        print 'log: %s inserted successfully'%result
        self.write(home_template.render({"name":name}))


#Sends the new user joined alerts to all subscribers who subscribed
@tornado.gen.coroutine
def send_user_alert():
    while True:
        try:
            temp_conn = yield r.connect(RDB_HOST,RDB_PORT,PROJECT_DB)

            feed = yield r.table("users").changes().run(temp_conn)

            while (yield feed.fetch_next()):
                new_user_alert = yield feed.next()
                print subscribers
                for subscriber in subscribers:
                    subscriber.write_message(new_user_alert)
        except:
            pass


class WSocketHandler(tornado.websocket.WebSocketHandler): #Tornado Websocket Handler

    def check_origin(self, origin):
        return True

    def open(self):
        self.stream.set_nodelay(True)
        subscribers.add(self) #Join client to our league

    def on_close(self):
        if self in subscribers:
            subscribers.remove(self) #Remove client


if __name__ == "__main__":
    dbSetup() #Check DB and Tables were pre created
    
    #Define tornado application
    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_folder = os.path.join(current_dir, 'static')
    tornado_app = tornado.web.Application([
    ('/', MainHandler), #For Landing Page
    (r'/ws', WSocketHandler), #For Sockets
    (r'/static/(.*)', tornado.web.StaticFileHandler, { 'path': static_folder }) #Define static folder       
    ])

    #Start the server
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(8000) #Bind port 8888 to server
    tornado.ioloop.IOLoop.current().add_callback(send_user_alert)
    tornado.ioloop.IOLoop.instance().start()
