import os, json
import re
from flask import Flask, request
from flask_pymongo import PyMongo
from flask import abort
from utils import object_id, unique_name

STATIC_FILE_LIST = ['recipe']
ALL_RECIPE_LIST = ['name', 'tags', 'location', 'description', 'comments']
DATABASE_NAME = 'mongodb://localhost:27017/what_to_eat_db'

app = Flask(__name__)
# setup database uri
app.config['MONGO_URI'] = DATABASE_NAME
mongo = PyMongo(app)

# database name: what_to_eat_db
# collection name: recipe
# document fields: _id(auto), name, price, star(number), tags(list), location, images(url-list), description, comments(list)

@app.route('/recipe/count/<string:key>')
def get_recipe_doc_count(key):
    name = request.args.get('query', '')
    query = {'{0}'.format(key): {'$regex':'{0}'.format(name)}}
    return {'counts': mongo.db.recipe.count_documents(query)}

@app.route('/recipe/post', methods=['POST'])
def post_recipe():
    recipe = mongo.db.recipe
    json_data = request.get_json()
    json_data['_id'] = object_id()
    recipe.insert_one(json_data)
    return 'success'

@app.route('/<string:path>/img', methods=['POST'])
def post_img(path):
    if path not in STATIC_FILE_LIST:
        return 'folder not found', 404
    upload_img = request.files['file']
    save_path = os.path.join('static', path, unique_name(upload_img.filename))
    upload_img.save(save_path)
    return save_path.replace('\\', '/')

@app.route('/recipe/update', methods=['POST'])
def update_comments():
    request_data = request.get_json()
    q_id = request_data['_id']
    comment = request_data['comment']
    query = {'_id': q_id }
    result_cursor = mongo.db.recipe.update_one(query, {'$addToSet': {'comments': comment}})
    if result_cursor is None: abort(404)
    return 'success'

@app.route('/recipe/find/<string:key>', methods=['GET'])
def search_recipe(key):
    name = request.args.get('query', '')
    last_uid = request.args.get('last_uid', type=int)
    limit = request.args.get('limit', 10, type=int)
    query = {'{0}'.format(key): {'$regex':'{0}'.format(name)}}
    if last_uid:
        query['_id'] = {'$lt': last_uid}
    result_cursor = mongo.db.recipe.find(query).sort('_id', -1).limit(limit)
    if result_cursor is None: abort(404)
    result_list = [i for i in result_cursor]
    return json.dumps(result_list)

@app.route('/recipe/findall', methods=['GET'])
def search_all_recipe():
    result_list = list()
    final_result = list()
    _id_list = list()
    for item in ALL_RECIPE_LIST:
        result_list.extend(json.loads(search_recipe(item)))
    for item in result_list:
        if item['_id'] in _id_list: continue
        _id_list.append(item['_id'])
        final_result.append(item)
    return json.dumps(final_result)
    


if __name__ == '__main__':
    app.run(debug=True) 
