from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with

app = Flask(__name__)
api = Api(app)

items = {}

def abort_if_item_doesnt_exist(item_id):
    if item_id not in items:
        abort(404, message="Item {} doesn't exist".format(item_id))

item_fields = {
    'name': fields.String,
    'description': fields.String,
}

class Item(Resource):
    @marshal_with(item_fields)
    def get(self, item_id):
        abort_if_item_doesnt_exist(item_id)
        return items[item_id]

    @marshal_with(item_fields)
    def put(self, item_id):
        args = request.get_json()
        item = {'name': args['name'], 'description': args['description']}
        items[item_id] = item
        return item, 201

    def delete(self, item_id):
        abort_if_item_doesnt_exist(item_id)
        del items[item_id]
        return '', 204

class ItemList(Resource):
    @marshal_with(item_fields)
    def get(self):
        return items

    @marshal_with(item_fields)
    def post(self):
        args = request.get_json()
        item_id = int(max(items.keys() or [0])) + 1
        items[item_id] = {'name': args['name'], 'description': args['description']}
        return items[item_id], 201

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/items/<int:item_id>')

if __name__ == '__main__':
    app.run(debug=True)
