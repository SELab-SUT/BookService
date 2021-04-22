import enum
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TransactionType(enum.Enum):
	CREATE = 0
	UPDATE = 1
	DELETE = 2

class Transaction(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	timestamp = db.Column(db.DateTime, server_default=db.func.now())
	admin = db.Column(db.String(15), nullable=False)
	transaction_type = db.Column(db.Enum(TransactionType), nullable=False)
	book_id = db.Column(db.Integer, nullable=False)
	book_title = db.Column(db.String(80))
	book_author = db.Column(db.String(80))
	book_price = db.Column(db.Integer)

	def to_dict(self):
		vals = vars(self)
		return {attr: str(vals[attr]) for attr in vals if 'instance_state' not in attr}
