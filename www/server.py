import tornado.ioloop
import tornado.web

from tornado.options import define, options, parse_command_line

define("port", default=8080, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/index.htm")


app = tornado.web.Application([
    (r'/', IndexHandler)
])

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()