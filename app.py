from flask import Flask, request, jsonify
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DATABASE_CONFIG
from models import Email, User
# from email_sender import send_custom_email

from flask import render_template
from datetime import datetime



# Initiate SQAlchemy
db = SQLAlchemy()

# Configure Flask app
def create_app():
    app = Flask(__name__)

    # configure database from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = f"{DATABASE_CONFIG['DRIVER']}://{DATABASE_CONFIG['USER']}:{DATABASE_CONFIG['PASSWORD']}@{DATABASE_CONFIG['HOST']}/{DATABASE_CONFIG['DATABASE']}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initiate SQLAlchemy and Flask-Migrate
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Route for URL show email datas in database
    @app.route('/')
    def view_emails():
        return render_template('view_emails.html')
    
    # Route for add new email data
    @app.route('/add_emails', methods=['GET'])
    def add_email_form():
        return render_template('add_email.html')
    
    # Define endpoint to save email
    @app.route('/save_emails', methods=['POST'])
    def save_emails():
        data = request.form
        event_id = data.get('event_id')
        email_subject = data.get('email_subject')
        email_content = data.get('email_content')
        timestamp_str = data.get('timestamp')
        
        # Convert timestamp string into datetime object
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M')
        
        email = Email(
            event_id=event_id,
            email_subject=email_subject,
            email_content=email_content,
            timestamp=timestamp
        )

        db.session.add(email)
        db.session.commit()
        
        email_data = {
            "Event Id": email.event_id,
            "Email Subject": email.email_subject,
            "Email Content": email.email_content,
            "Timestamp": email.timestamp.strftime('%Y-%m-%d %H:%M')
        }
        
        return jsonify({"message": "Email successfully saved", "email": email_data}), 201
    
    
    # Route for add new User/Recipient
    @app.route('/add_user', methods=['GET'])
    def add_user_form():
        return render_template('add_user.html')
    
    # Define endpoint to save new User/Recipient
    @app.route('/save_user', methods=['POST'])
    def save_user():
        data = request.form
        fullname = data.get('fullname')
        email = data.get('email')
        
        user = User(
            fullname=fullname,
            email=email,
        )

        db.session.add(user)
        db.session.commit()
        
        User_data = {
            "Fullname": user.fullname,
            "Email": user.email,
        }
        
        return jsonify({"message": "User successfully added", "user": User_data}), 201
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)