from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be blank!")
    parser.add_argument('store_id', type=int, required=True, help="each item most have an id")

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': "item not found"}, 404

    @staticmethod
    def post(name):
        if ItemModel.find_by_name(name):
            return {"message": "Item is already exits!"}, 400
        data_in = Item.parser.parse_args()
        item = ItemModel(name, **data_in)
        try:
            item.save_to_db()
        except:
            return {"message": "An error happend while inserting"}, 500
        return {"message": "Item added", "item": item.json()}, 200

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'item have been deleted'}, 200
        return {'message': 'Item did not exist!'}, 400

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json(), 200


class ItemList(Resource):
    def get(self):
        """connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        rows = result.fetchall()
        items = []
        for row in rows:
            items.append({'name': row[1], 'price': row[2]})
        connection.close()
        return {'items': items}, 200"""
        return {'items': [item.json() for item in ItemModel.find_all()]}
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
