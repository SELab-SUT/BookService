from flask import Flask, request
from flask.json import jsonify
from sqlalchemy.exc import IntegrityError
from http import HTTPStatus
from models import *
from event_handler import bus

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_BINDS'] = {
	'transactions': 'sqlite:///transactions.sqlite3',
	'books': 'sqlite:///books.sqlite3'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False	# To silence a warning

@app.before_first_request
def setup_db():
	db.init_app(app)
	db.create_all()


@app.route('/books/create', methods=['POST'])
def create_book():
	data = request.json
	# TODO: Needs better checking
	if 'book_id' in data and Transaction.query.filter_by(book_id=data['book_id']).first():
		return {'message': 'Error: Book already exists!'}, HTTPStatus.CONFLICT

	transaction = Transaction(admin=data.get('admin'),
								transaction_type=TransactionType['CREATE'],
								book_id=data.get('book_id'),
								book_title=data.get('book_title'),
								book_author=data.get('book_author'),
								book_price=data.get('book_price'))
	try:
		db.session.add(transaction)
		db.session.commit()
		bus.emit('create:book', transaction)
		return {'message': 'Ok'}, HTTPStatus.CREATED
	except IntegrityError:
		return {'message': 'Bad Request'}, HTTPStatus.BAD_REQUEST


@app.route('/books/update/<int:book_id>', methods=['PUT'])
def update_book(book_id):
	data = request.json
	# TODO: Needs better checking
	if Transaction.query.filter_by(book_id=book_id).first() is None:
		return {'message': 'Error: No such book found!'}, HTTPStatus.NOT_FOUND

	transaction = Transaction(admin=data.get('admin'),
								transaction_type=TransactionType['UPDATE'],
								book_id=book_id,
								book_title=data.get('book_title'),
								book_author=data.get('book_author'),
								book_price=data.get('book_price'))

	try:
		db.session.add(transaction)
		db.session.commit()
		bus.emit('update:book', transaction)
		return {'message': 'Ok'}, HTTPStatus.OK
	except IntegrityError:
		return {'message': 'Bad Request'}, HTTPStatus.BAD_REQUEST


@app.route('/books/delete/<int:book_id>', methods=['PUT'])
def delete_book(book_id):
	data = request.json
	# TODO: Needs better checking
	if Transaction.query.filter_by(book_id=book_id).first() is None:
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


@app.route('/books/log', methods=['GET'])
def show_transactions():
	return jsonify([tr.to_dict() for tr in Transaction.query.all()])


if __name__ == '__main__':
	app.run()
