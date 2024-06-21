from flask import Flask, request, current_app
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
api = Api(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./items.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'items.db')
db = SQLAlchemy(app)

class ItemModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"Item(name={self.name}, description={self.description})"

# 데이터베이스 생성을 애플리케이션 컨텍스트 내부로 이동
with app.app_context():
    db.create_all()

item_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
}

class Item(Resource):
    @marshal_with(item_fields)
    def get(self, item_id):
        item = ItemModel.query.filter_by(id=item_id).first()
        if not item:
            abort(404, message="Item {} doesn't exist".format(item_id))
        return item

    @marshal_with(item_fields)
    def put(self, item_id):
        args = request.get_json()
        item = ItemModel.query.filter_by(id=item_id).first()
        if item:
            item.name = args['name']
            item.description = args['description']
        else:
            item = ItemModel(id=item_id, name=args['name'], description=args['description'])
            db.session.add(item)
        db.session.commit()
        return item, 201

    def delete(self, item_id):
        item = ItemModel.query.filter_by(id=item_id).first()
        if not item:
            abort(404, message="Item {} doesn't exist".format(item_id))
        db.session.delete(item)
        db.session.commit()
        return '', 204

class ItemList(Resource):
    @marshal_with(item_fields)
    def get(self):
        items = ItemModel.query.all()
        return items

    @marshal_with(item_fields)
    def post(self):
        args = request.get_json()
        item = ItemModel(name=args['name'], description=args['description'])
        db.session.add(item)
        db.session.commit()
        return item, 201

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/items/<int:item_id>')

if __name__ == '__main__':
    app.run(debug=True)
