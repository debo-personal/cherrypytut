import os, os.path
import string 
import random
import cherrypy
import sqlite3
import time

DB_STRING = 'my.db'

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return open('index.html')

@cherrypy.expose
class StringGeneratorWebService(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        with sqlite3.connect(DB_STRING) as con:
            cherrypy.session['ts'] = time.time()
            result = con.execute("SELECT value FORM use_string where session_id=?",[cherrypy.session.id])
            return result.fetchone()

    def POST(self, length = 8):
        random_string = ''.join(random.sample(string.hexdigits, int(length)))
        with sqlite3.connect(DB_STRING) as con:
            cherrypy.session['ts'] = time.time()
            con.execute("INSERT INTO user_string VALUES(?,?)",[cherrypy.session.id, random_string])
        return random_string

    def PUT(self, new_string):
        with sqlite3.connect(DB_STRING) as con:
            cherrypy.session['ts'] = time.time()
            con.execute("UPDATE user_string SET value=? WHERE session_id=?",[new_string, cherrypy.session.id])

    def DELETE(self):
        cherrypy.session.pop('ts', None)
        with sqlite3.connect(DB_STRING) as con:
            con.execute("DELETE FROM user_string WHERE session_id=?", [cherrypy.session.id])
        

def setup_database():
    '''Create the 'user_string' table in the database on server startup'''
    with sqlite3.connect(DB_STRING) as con:
        con.execute("CREATE TABLE user_string (session_id, value)")

def cleanup_database():
    '''Drop the database on server stop'''
    with sqlite3.connect(DB_STRING) as con:
        con.execute("DROP TABLE user_string")

if __name__ == '__main__':
    conf = {
        '/' : {
            'tools.sessions.on' : True,
            'tools.staticdir.root' : os.path.abspath(os.getcwd())
        },
        '/generator' : {
            'tools.response_headers.on' : True,
            'tools.response_headers.headers' : [('Content-Type', 'text/plain')],
            'request.dispatch' : cherrypy.dispatch.MethodDispatcher()
        },
        '/static' : {
            'tools.staticdir.on' : True,
            'tools.staticdir.dir' : 'public'
        }
    }

    cherrypy.engine.subscribe('start', setup_database)
    cherrypy.engine.subscribe('stop', cleanup_database)

    webapp = StringGenerator()
    webapp.generator = StringGeneratorWebService()
    cherrypy.quickstart(webapp, '/', conf)