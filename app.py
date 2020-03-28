
import os
from notion.client import NotionClient
from flask import Flask
from flask import request


import pprint


class LoggingMiddleware(object):
    def __init__(self, app):
        self._app = app
    def __call__(self, environ, resp):
        errorlog = environ['wsgi.errors']
        pprint.pprint(('REQUEST', environ), stream=errorlog)
        def log_response(status, headers, *args):
            pprint.pprint(('RESPONSE', status, headers), stream=errorlog)
            return resp(status, headers, *args)
        return self._app(environ, log_response)





app = Flask(__name__)

def createNotionRowGeneric(token, collectionURL, request_keys):
    # notion
    client = NotionClient(token)
    print('notion-url- {}'.format(collectionURL))
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    notion_keys = row.get_all_properties().keys()
    for key in intersection(request_keys,notion_keys):
        print('key - {} -'.format(key))
        setattr(row, key, request.args.get(key)) 



@app.route('/create_row', methods=['GET'])
def add_generic():
    print(request.headers)
    token_v2 = os.environ.get("TOKEN")
    url = request.headers.get('notionurl')
    request_keys = request.headers.keys()
    createNotionRowGeneric(token_v2, url, request_keys )
    return f'added {todo} to Notion'



if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    app.run(host='0.0.0.0', port=port)
