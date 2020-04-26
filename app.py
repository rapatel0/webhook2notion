
import os
from notion.client import NotionClient
from notion.block  import TextBlock
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

def return_row(uid, rows):
    dd = []
    for r in rows:
         if r.UID == uid:
            dd.append(r)
    if not dd:
        return



app = Flask(__name__)

def createNotionRowGeneric(token, collectionURL, request):
    # notion
    client = NotionClient(token)
    print('notion-url- {}'.format(collectionURL))
    cv  = client.get_collection_view(collectionURL)
    request_dict = dict(request.headers)
    request_keys = set(request_dict.keys())
    uid = request.headers.get('uid')
    match_rows = []
    for r in cv.collection.get_rows():
        if uid == r.UID:
            match_rows.append(r)
    dd = cv.collection.query() ## hack to initialize the view
    if not match_rows:
        row = cv.collection.add_row()
    else:
        ## Ignore all other matched rows
        row = match_rows[0]

    notion_keys = set([i.capitalize() for i in list(row.get_all_properties().keys())])
    for key in (request_keys & notion_keys):
        print('key - {} -'.format(key))
        setattr(row, key, request.headers.get(key))
    data = dict(request.get_json())
    for key in data:
        row.children.add_new(TextBlock, title=data[key])


@app.route('/create_row', methods=['GET', 'POST'])
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
