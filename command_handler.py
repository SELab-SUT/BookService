from flask import Blueprint, request
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from http import HTTPStatus
from models import *
from event_handler import bus

command_handler = Blueprint('Command Handler', __name__)

def book_exists(book_id):
	transaction = Transaction.query.filter_by(book_id=book_id) \
									.order_by(desc(Transaction.timestamp)) \
									.limit(1).first()
	return transaction is not None and \
			transaction.transaction_type != TransactionType['DELETE']


@command_handler.route('/books/create', methods=['POST'])
def create_book():
	data = request.json
	if 'book_id' in data and book_exists(data['book_id']):
		return {'message': 'Error: Book already exists!'}, HTTPStatus.CONFLICT

	transaction = Transaction(admin=data.get('admin'),
								transaction_type=TransactionType['CREATE'],
								book_id=data.get('book_id'),
								book_title=data.get('book_title'),
								book_category=data.get('book_category'),
								book_author=data.get('book_author'),
								book_price=data.get('book_price'))
	try:
		db.session.add(transaction)
		db.session.commit()
		bus.emit('create:book', transaction)
		return {'message': 'Ok'}, HTTPStatus.CREATED
	except IntegrityError:
		return {'message': 'Bad Request'}, HTTPStatus.BAD_REQUEST


@command_handler.route('/books/update/<int:book_id>', methods=['PUT'])
def update_book(book_id):
	data = request.json
	if not book_exists(book_id):
		return {'message': 'Error: No such book found!'}, HTTPStatus.NOT_FOUND

	transaction = Transaction(admin=data.get('admin'),
								transaction_type=TransactionType['UPDATE'],
								book_id=book_id,
								book_title=data.get('book_title'),
								book_category=data.get('book_category'),
								book_author=data.get('book_author'),
								book_price=data.get('book_price'))

	try:
		db.session.add(transaction)
		db.session.commit()
		bus.emit('update:book', transaction)
		return {'message': 'Ok'}, HTTPStatus.OK
	except IntegrityError:
		return {'message': 'Bad Request'}, HTTPStatus.BAD_REQUEST


@command_handler.route('/books/delete/<int:book_id>', methods=['PUT'])
def delete_book(book_id):
	data = request.json
	if not book_exists(book_id):
		return {'message': 'Error: No such book found!'}, HTTPStatus.NOT_FOUND

	transaction = Transaction(admin=data.get('admin'),
								transaction_type=TransactionType['DELETE'],
								book_id=book_id)

	try:
		db.session.add(transaction)
		db.session.commit()
		bus.emit('delete:book', transaction)
		return {'message': 'Ok'}, HTTPStatus.OK
	except IntegrityError:
		return {'message': 'Bad Request'}, HTTPStatus.BAD_REQUEST
