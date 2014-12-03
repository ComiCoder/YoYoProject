import sys
import os

from tornado.options import options, define, parse_command_line
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi

from django.core.wsgi import get_wsgi_application
import YoYoProject
#sys.path.append('/home/lawgon/') # path to your project ( if you have it in another dir).

define('port', type=int, default=8080)

def main():
    print 'start django with tornado'
    os.environ['DJANGO_SETTINGS_MODULE'] = 'YoYoProject.settings' # path to your settings module
    #application = django.core.handlers.wsgi.WSGIHandler()
    application = get_wsgi_application()
    print 'start django'
    
    print  YoYoProject.settings.BASE_DIR
    print YoYoProject.settings.STATICFILES_DIRS
    
    
    container = tornado.wsgi.WSGIContainer(application)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(8888)
    
    print "start tornado"
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()