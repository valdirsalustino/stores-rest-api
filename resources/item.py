from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('price', type=float, required=True, help='This field cannot be left blank!')
	parser.add_argument('store_id', type=int, required=True, help='Every item needs a store_id')

	@jwt_required()
	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json(), 200
		return {'message': 'Item not found'}, 404

	@jwt_required()
	def post(self, name):
		if ItemModel.find_by_name(name):
			return {'message': f'An item with name \'{name}\' already exists.'}, 400
		data = Item.parser.parse_args()
		item = ItemModel(name, **data)
		try:
			item.save_to_db()
		except: 
			return {'message': 'an error occurr inserting the data'}, 500 # internal server error
		return item.json(), 201

	@jwt_required()
	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()

		return {'message': 'Item deleted'}

	# Observe put can be used to create or update an item
	@jwt_required()
	def put(self, name):
		data = Item.parser.parse_args()

		item = ItemModel.find_by_name(name)
		if item is None:
			item = ItemModel(name, **data)
		else:
			item.price = data['price']

		item.save_to_db()
		return item.json()


class ItemList(Resource):
	@jwt_required()
	def get(self):
		return {'items:': [i.json() for i in ItemModel.query.all()]}
