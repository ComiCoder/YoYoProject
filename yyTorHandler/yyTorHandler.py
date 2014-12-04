'''

@author: ryu
'''
import tornado
class YYTornadoHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello!")
        
    