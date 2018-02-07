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
        return ''.join(random.sample(string.hexdigits, int(length)))

if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld())