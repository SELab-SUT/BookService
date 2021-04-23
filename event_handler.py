from event_bus import EventBus
from models import db, Book

bus = EventBus()

@bus.on('create:book')
def handle_create_book(transaction):
	book = Book(id=transaction.book_id, title=transaction.book_title,
				category=transaction.book_category, 
				author=transaction.book_author, price=transaction.book_price)
	db.session.add(book)
	db.session.commit()

@bus.on('update:book')
def handle_update_book(transaction):
	book = Book.query.get(transaction.book_id)
	if transaction.book_title is not None:
		book.title = transaction.book_title
	if transaction.book_category is not None:
		book.category = transaction.book_category
	if transaction.book_author is not None:
		book.author = transaction.book_author
	if transaction.book_price is not None:
		book.price = transaction.book_price
	db.session.commit()

@bus.on('delete:book')
def handle_delete_book(transaction):
	book = Book.query.get(transaction.book_id)
	db.session.delete(book)
	db.session.commit()
