from flask import Blueprint, request
from flask.json import jsonify
from models import *

query_handler = Blueprint('Query Handler', __name__)

@query_handler.route('/books/q', methods=['GET'])
def get_books():
	query = Book.query
	if 'title' in request.args:
		query = query.filter(Book.title.ilike("%" + request.args['title'] + "%"))
	if 'category' in request.args:
		query = query.filter_by(category=request.args['category'])

	return jsonify([book.to_dict() for book in query.all()])
