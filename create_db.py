from app import create_app

app = create_app()
from app import db

with app.app_context():
    db.create_all()
    print("Tables created successfully")
