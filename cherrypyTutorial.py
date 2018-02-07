import cherrypy
import random
import string

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return '''
        <html>
            <head></head>
            <body>
                <form action="generate" method="GET">
                    <input type="text" name="length" value="8"/>
                    <button type="submit">Submit</button>
                </form>
            </body>
        </html>
        '''
    
    @cherrypy.expose
    def generate(self, length=8):
        random_string = ''.join(random.sample(string.hexdigits, int(length)))
        cherrypy.session['random_string'] = random_string
        return random_string

    @cherrypy.expose
    def display(self):
        return cherrypy.session['random_string']

if __name__ == '__main__':
    conf = {
        '/' : {
            'tools.sessions.on' : True
        }
    }
    cherrypy.quickstart(HelloWorld(), '/', conf)