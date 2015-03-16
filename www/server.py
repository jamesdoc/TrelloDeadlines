import tornado.ioloop
import tornado.web
import tornado.autoreload
import requests
from tornado.options import define, options, parse_command_line
from config import config
from os import path, environ, walk
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from operator import itemgetter
import datetime

define("port", default=8080, help="run on the given port", type=int)

CARDS_IN_BOARDS_URL = "https://api.trello.com/1/boards/%s/cards/open?key=%s&token=%s"

class TemplateRendering(object):

    def render_template(self, template_name, variables):
        template_dirs = ['templates']
        template_dirs.append(path.join(path.dirname(__file__), 'templates')) # added a default for fail over.
        env = Environment(loader = FileSystemLoader(template_dirs))
        try:
            template = env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)
        content = template.render(variables)
        return content


class IndexHandler(tornado.web.RequestHandler, TemplateRendering):
    def get(self):
        cards_raw = self.get_cards_for_list_of_boards(config['boards'])

        if type(cards_raw) is unicode:
            self.display_error(cards_raw)
            return

        cards_with_dates = self.get_cards_with_due_dates(cards_raw)
        cards_sorted = sorted(cards_with_dates, key=itemgetter('due'))
        cards_timeboxed = self.sort_cards_into_timeboxes(cards_sorted)

        data = {
            'cards': self.get_cards_with_due_dates(cards_sorted),
            'timeboxed': cards_timeboxed
        }

        content = self.render_template('index.htm', data)
        self.write(content)

    def display_error(self, msg):
        self.write('<h1>%s</h1>' % msg)

    def sort_cards_into_timeboxes(self, cards):
        timebox = {'past': [], 'this_week': [], 'thirty_days': [], 'radar': []}
        today = datetime.datetime.now()

        date_today = today.date()
        date_seven_days = date_today - datetime.timedelta(-7)
        date_thirty_days = date_today - datetime.timedelta(-30)

        for card in cards:
            card['due'] = datetime.datetime.strptime(card['due'], "%Y-%m-%dT%H:%M:%S.%fZ")

            date_card = card['due'].date()

            if date_card < today.date():
                timebox['past'].append(card)
            elif date_card <= date_seven_days:
                timebox['this_week'].append(card)
            elif date_card <= date_thirty_days:
                timebox['thirty_days'].append(card)
            else:
                timebox['radar'].append(card)
        return timebox

    def get_cards_for_list_of_boards(self, boards):
        cards = []
        for board in boards:
            board_cards = self.get_cards_from_board(board)

            # If the Trello API returns an error it comes back as unicode.
            if type(board_cards) is unicode:
                return board_cards

            cards = cards + board_cards
        return cards

    def get_cards_with_due_dates(self, cards):
        rtn_cards = []
        for card in cards:
            if card['due']:
                rtn_cards.append(card)
        return rtn_cards

    def cards_in_board_url(self, board_id):
        return CARDS_IN_BOARDS_URL % (board_id, config['key'], config['token'])

    def get_cards_from_board(self, board_id):
        url = self.cards_in_board_url(board_id)
        return self.talk_to_api(url)

    def talk_to_api(self, url):
        r = requests.get(url)
        try:
            return r.json()
        except ValueError:
            return r.text



app = tornado.web.Application([
    (r'/', IndexHandler),
])

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)

    if config['development'] is True:
        tornado.autoreload.start()
        for dir, _, files in walk('templates'):
            [tornado.autoreload.watch(dir + '/' + f) for f in files if not f.startswith('.')]

    tornado.ioloop.IOLoop.instance().start()