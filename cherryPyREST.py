import string 
import random
import cherrypy

@cherrypy.expose
class StringGeneratorWebService(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return cherrypy.session['random_string']

    def POST(self, length = 8):
        random_string = ''.join(random.sample(string.hexdigits, int(length)))
        cherrypy.session['random_string'] = random_string
        return random_string

    def PUT(self, new_string):
        cherrypy.session['random_string'] = new_string

    def DELETE(self):
        cherrypy.session.pop('random_string', None)

if __name__ == '__main__':
    conf = {
        '/' : {
            'tools.sessions.on' : True,
            'tools.response_headers.on' : True,
            'tools.response_headers.headers' : [('Content-Type', 'text/plain')],
            'request.dispatch' : cherrypy.dispatch.MethodDispatcher()
        }
    }
    cherrypy.quickstart(StringGeneratorWebService(), '/', conf)