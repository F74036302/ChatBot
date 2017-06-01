import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine


API_TOKEN = '385435814:AAENCkCXqxpodljusFzoAvTrqWXCFMQAx80'
WEBHOOK_URL = 'https://4db79113.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'severType',
        'orderS',
        'bookS',
		'recommendS',
        'OAS',
        'OBS',
        'OCS',
        'OcheckS',
        'BcheckS',
        'BrefuseS',
        'Start'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'severType',
            'dest': 'orderS',
            'conditions': 'select_order'
        },
        {
            'trigger': 'advance',
            'source': 'severType',
            'dest': 'bookS',
            'conditions': 'select_book'
        },
        {
            'trigger': 'advance',
            'source': 'severType',
            'dest': 'recommendS',
            'conditions': 'select_recommend'
        },
        {
            'trigger': 'go_back',
            'source': 'recommendS',
            'dest': 'severType'
        },
        {
            'trigger': 'advance',
            'source': 'orderS',
            'dest': 'OAS',
            'conditions': 'select_A'
        },
        {
            'trigger': 'advance',
            'source': 'orderS',
            'dest': 'OBS',
            'conditions': 'select_B'
        },
        {
            'trigger': 'advance',
            'source': 'orderS',
            'dest': 'OCS',
            'conditions': 'select_C'
        },
        {
            'trigger': 'advance',
            'source': [
                'OAS',
                'OBS',
                'OCS'
            ],
            'dest': 'OcheckS',
            'conditions': 'select_check'
        },
        {
            'trigger': 'go_back',
            'source': 'OcheckS',
            'dest': 'severType'
        },
        {
            'trigger': 'advance',
            'source': 'bookS',
            'dest': 'BcheckS',
            'conditions': 'select_bookcheck'
        },
        {
            'trigger': 'advance',
            'source': 'bookS',
            'dest': 'BrefuseS',
            'conditions': 'select_bookcheck2'
        },
        {
            'trigger': 'go_back',
            'source': [
                'BcheckS',
                'BrefuseS',
                'Start'],
            'dest': 'severType'
        },
        {
            'trigger': 'advance',
            'source': 'severType',
            'dest': 'Start',
            'conditions': 'start_chat'
        }
    ],
    initial='severType',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()
