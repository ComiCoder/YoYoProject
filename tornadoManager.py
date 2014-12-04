import sys
import os

from tornado.options import options, define, parse_command_line
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi

from django.core.wsgi import get_wsgi_application
import YoYoProject
from yyTorHandler.yyTorHandler import YYTornadoHandler
#sys.path.append('/home/lawgon/') # path to your project ( if you have it in another dir).

define('port', type=int, default=8000)

def main():
    
    os.environ['DJANGO_SETTINGS_MODULE'] = 'YoYoProject.settings' # path to your settings module
    #application = django.core.handlers.wsgi.WSGIHandler()
    wsgi_app  = get_wsgi_application()
    container = tornado.wsgi.WSGIContainer(wsgi_app)
    
    
    settings = dict(
            #template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )
    
    tornado_app = tornado.web.Application(
        [
            ('/hello-tornado', YYTornadoHandler),
            ('.*', tornado.web.FallbackHandler, dict(fallback=container)),
        ], **settings)
    
   #container = tornado.wsgi.WSGIContainer(tornado_app)
    http_server = tornado.httpserver.HTTPServer(tornado_app)
    http_server.listen(options.port)
    
    print "start tornado"
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()