## import CRUD Operations from ORM Lesson
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"

                output += "<h1>Hello!</h1><a href = '/hola'> Spanish Version</a>"
                #<a href = '/hola'> Spanish Version</a><

                output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
                output += "<h2>What would you like me to say back to you?</h2>"
                output += "<input name='message' type='text'>"
                output += "<input type='submit' value = 'Submit' </form>"

                output += "</body></html>"
                self.wfile.write(output.encode('utf-8'))
                print(output)
                return
            elif self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"

                output += "<h1>&#161Hola!</h1><a href = '/hello'> English Version</a>"
                #<a href = '/hello'> English Version</a><

                output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
                output += "<h2>What would you like me to say back to you?</h2>"
                output += "<input name='message' type='text'>"
                output += "<input type='submit' value='Submit'></form>"

                output += "</body></html>"
                self.wfile.write(output.encode('utf-8'))
                print(output)
                return
            elif self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<a href = '/restaurants/new'>Make a New Restaurant Here</a></br>"
                output += "<h1>Restaurants List</h1>"
                output += "<style>h3 {display: inline;}</style>"
                for restaurant in session.query(Restaurant).all():
                    output += "<h3>%s</h3></br>" % restaurant.name
                    output += "<a href = '/restaurants/%s/edit'>Edit</a></br>" % restaurant.id
                    output += "<a href = '/restaurants/%s/delete'>Delete</a></br>" % restaurant.id
                    output += "</br>"
                output += "</body></html>"
                self.wfile.write(output.encode('utf-8'))
                print(output)
                return
            elif self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(bytes(output, "UTF-8"))
                return
            elif self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                id_num = self.path.split('/')[2]
                restaurant = session.query(Restaurant).filter_by(id = id_num).one()
                output = ""
                output += "<html><body>"
                output += "<h2>%s</h2>" % restaurant.name
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/%s/edit'>" % id_num
                output += "<input name = 'editRestaurantName' type = 'text' placeholder = '%s' > " % restaurant.name
                output += "<input type='submit' value='Rename'>"
                output += "</form></body></html>"
                self.wfile.write(bytes(output, "UTF-8"))
                return
            elif self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                id_num = self.path.split('/')[2]
                restaurant = session.query(Restaurant).filter_by(id = id_num).one()
                output = ""
                output += "<html><body>"
                output += "<h1>Are you sure you want to delete %s?</h1>" % restaurant.name
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/%s/delete'>" % id_num
                output += "<input type='submit' value='Delete'>"
                output += "</form></body></html>"
                self.wfile.write(bytes(output, "UTF-8"))
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                pdict['boundary'] = bytes(pdict['boundary'], "utf - 8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                print(messagecontent[0])
                print(messagecontent[0].decode("utf-8"))
                newRestaurant = Restaurant(name = messagecontent[0].decode("utf-8"))
                session.add(newRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return
            elif self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                pdict['boundary'] = bytes(pdict['boundary'], "utf - 8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('editRestaurantName')
                print(messagecontent[0])
                id_num = self.path.split('/')[2]
                edittedRestaurant = session.query(Restaurant).filter_by(id = id_num).one()
                edittedRestaurant.name = messagecontent[0].decode("utf-8")
                session.add(edittedRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return
            elif self.path.endswith("/delete"):
                id_num = self.path.split('/')[2]
                deletedRestaurant = session.query(Restaurant).filter_by(id = id_num).one()
                session.delete(deletedRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return

            """ 
            #hello code output
            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            self.wfile.write(bytes(output, "UTF-8"))
            self.wfile.write(messagecontent[0])
            output = ""
            output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
            output += "<h2>What would you like me to say back to you?</h2>"
            output += "<input name='message' type='text'>"
            output += "<input type='submit' value = 'Submit' </form>"

            output += "</body></html>"
            self.wfile.write(output.encode('utf-8'))
            print(output)
            """


        except Exception as e:
            print(e)

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print("Web server running on port %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print(" entered, stopping web server now...")
        server.socket.close()


if __name__ == '__main__':
    main()