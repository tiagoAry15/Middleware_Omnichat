import tornado.ioloop
import tornado.web
import tornado.websocket


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message("You said: " + message)

    def on_close(self):
        print("WebSocket closed")

    def check_origin(self, origin):
        return True  # Allow all origins


class ConversationHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")  # Allow requests from any origin
        self.set_header("Access-Control-Allow-Methods", "GET")  # Allow only GET requests

    def get(self):
        # Define your logic to return all conversations
        self.write("All conversations")


def __main():
    app = tornado.web.Application([
        (r"/websocket", WebSocketHandler),
        (r"/get_all_conversations", ConversationHandler),
    ])
    port = 3000
    app.listen(port)
    print(f"Tornado server started at port {port}")
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    __main()
