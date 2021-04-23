from flask import Flask, request
from flask.json import jsonify
from models import *
from command_handler import command_handler
from query_handler import query_handler


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.register_blueprint(command_handler)
app.register_blueprint(query_handler)
app.config['SQLALCHEMY_BINDS'] = {
	'transactions': 'sqlite:///transactions.sqlite3',
	'books': 'sqlite:///books.sqlite3'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False	# To silence a warning

@app.before_first_request
def setup_db():
	db.init_app(app)
	db.create_all()

@app.route('/books/log', methods=['GET'])
def show_transactions():
	return jsonify([tr.to_dict() for tr in Transaction.query.all()])


if __name__ == '__main__':
	app.run()
