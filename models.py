from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Model for storing email data"
class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer)
    email_subject = db.Column(db.String(250))
    email_content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    
    def __repr__(self):
        return f"<Email {self.id}>"
    
# Model for storing user/recipient data"
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    
    def __repr__(self):
        return f"<User {self.id} - {self.fullname}"