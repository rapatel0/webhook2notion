
import os
from notion.client import NotionClient
from flask import Flask
from flask import request


app = Flask(__name__)

def createNotionRowGeneric(token, collectionURL, request):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    for key in request.args.keys():
        setattr(row, key, request.args.get(key)) 



@app.route('/create_row', methods=['GET'])
def add_generic():
    token_v2 = os.environ.get("TOKEN")
    url = request.args.get('notionurl')
    createNotionRowGeneric(token_v2, url, request )
    return f'added {todo} to Notion'



if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
