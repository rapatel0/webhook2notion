
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

def createNotionRowGeneric(token, collectionURL, request):
    # notion
    client = NotionClient(token)
    print('notion-url- {}'.format(collectionURL))
    cv = client.get_collection_view(collectionURL)
    
    dd = cv.collection.query() ## hack to initialize the view
    row = cv.collection.add_row()
    request_dict = dict(request.headers)
    request_keys = set(request_dict.keys())
    notion_keys = set([i.capitalize() for i in list(row.get_all_properties().keys())])
    for key in (request_keys & notion_keys):
        print('key - {} -'.format(key))
        setattr(row, key, request.headers.get(key)) 



@app.route('/create_row', methods=['GET'])
def add_generic():
    print(request.headers)
    token_v2 = os.environ.get("TOKEN")
    url = request.headers.get('notionurl') 
    createNotionRowGeneric(token_v2, url, request )
    return f'added row to Notion'



if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    app.run(host='0.0.0.0', port=port)
