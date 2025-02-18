import click, sys
from models import db, User
from app import app
from sqlalchemy.exc import IntegrityError

@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    """Initializes the database and adds a test user."""
    with app.app_context():  
        db.drop_all()
        db.create_all()

        try:
            bob = User(username='bob', email='bob@mail.com', password='bobpass')
            db.session.add(bob)  
            db.session.commit()  
            print(f"User created: {bob}")
        except IntegrityError as e:
            db.session.rollback()  
            print(f"Error creating user: {e}")

        print("Database initialized")


@app.cli.command("get-user", help="Retrieves a User")
@click.argument('username', default='bob')
def get_user(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} not found!')
    return
  print(bob)

@app.cli.command('get-users')
def get_users():
      # gets all objects of a model
      users = User.query.all()
      print(users)

@app.cli.command("change-email")
@click.argument('username', default='bob')
@click.argument('email', default='bob@mail.com')
def change_email(username, email):
  bob = User.query.filter_by(username=username).first()
  if not bob:
      print(f'{username} not found!')
      return
  bob.email = email
  db.session.add(bob)
  db.session.commit()
  print(bob)

@app.cli.command('create-user')
@click.argument('username', default='rick')
@click.argument('email', default='rick@mail.com')
@click.argument('password', default='rickpass')
def create_user(username, email, password):
  newuser = User(username, email, password)
  try:
    db.session.add(newuser)
    db.session.commit()
  except IntegrityError as e:
    #let's the database undo any previous steps of a transaction
    db.session.rollback()
    # print(e.orig) #optionally print the error raised by the database
    print("Username or email already taken!") #give the user a useful message
  else:
    print(newuser) # print the newly created user


@app.cli.command('delete-user')
@click.argument('username', default='bob')
def delete_user(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
      print(f'{username} not found!')
      return
  db.session.delete(bob)
  db.session.commit()
  print(f'{username} deleted')