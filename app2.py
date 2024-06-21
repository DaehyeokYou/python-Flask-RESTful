from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with

app = Flask(__name__)
api = Api(app)

items = []
current_id = 1

def abort_if_item_doesnt_exist(item_id):
    if not any(item['id'] == item_id for item in items):
        abort(404, message="Item {} doesn't exist".format(item_id))

item_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
}

class Item(Resource):
    @marshal_with(item_fields)
    def get(self, item_id):
        abort_if_item_doesnt_exist(item_id)
        item = next(item for item in items if item['id'] == item_id)
        return item

    @marshal_with(item_fields)
    def put(self, item_id):
        args = request.get_json()
        item = next((item for item in items if item['id'] == item_id), None)
        if item is not None:
            item['name'] = args['name']
            item['description'] = args['description']
        else:
            item = {'id': item_id, 'name': args['name'], 'description': args['description']}
            items.append(item)
        return item, 201

    def delete(self, item_id):
        global items
        abort_if_item_doesnt_exist(item_id)
        items = [item for item in items if item['id'] != item_id]
        return '', 204

class ItemList(Resource):
    @marshal_with(item_fields)
    def get(self):
        return items

    @marshal_with(item_fields)
    def post(self):
        global current_id
        args = request.get_json()
        item = {'id': current_id, 'name': args['name'], 'description': args['description']}
        items.append(item)
        current_id += 1
        return item, 201

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/items/<int:item_id>')

if __name__ == '__main__':
    app.run(debug=True)
