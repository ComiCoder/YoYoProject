from tornado import websocket
class YYWebSocketHandler(websocket.WebSocketHandler):
    
    def check_origin(self, origin):
        return True

    def open(self):
        print 'websocket open'
    
    def on_message(self, message):
        self.write_message(u"You Said" + message)
        
    def on_close(self):
        print 'websocket close'