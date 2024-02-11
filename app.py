from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DATABASE_CONFIG
from models import Email, User, db, Scheduled_Email
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired

from celery_config import make_celery


# Configure Flask app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # configure database from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = f"{DATABASE_CONFIG['DRIVER']}://{DATABASE_CONFIG['USER']}:{DATABASE_CONFIG['PASSWORD']}@{DATABASE_CONFIG['HOST']}/{DATABASE_CONFIG['DATABASE']}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initiate SQLAlchemy and Flask-Migrate
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Initiate Celery in app
    
    global celery
    celery = make_celery(app)
    
    # Form to select email and user when sending email
    class SendEmailForm(FlaskForm):
        email = SelectField('Email', validators=[DataRequired()])
        user = SelectField('User', validators=[DataRequired()])
        
    # Task to send emails based on timestamp
    @celery.task
    def send_emails():
        emails = Email.query.filter(Email.timestamp <= datetime.now()).all()
        for email in emails:
            user = User.query.get(email.recipient_id)
    
    # Route for URL show email datas in database
    @app.route('/')
    def view_emails():
        # Get data from database
        emails = Email.query.all()
        users = User.query.all()
        scheduled_emails = Scheduled_Email.query.all()
        form = SendEmailForm()
        
        return render_template('view_emails.html', emails=emails, users=users, scheduled_emails=scheduled_emails, form=form, show_send_email_form=True)
    
    # Route for add new email data
    @app.route('/add_emails', methods=['GET'])
    def add_email_form():
        return render_template('add_email.html')
    
    # Define endpoint to save email
    @app.route('/save_emails', methods=['POST'])
    def save_emails():
        data = request.json
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
    
    # For send email to the user/recipient
    @app.route('/send_email', methods=['POST'])
    def send_email():
        email_id = request.form.get('email_id')
        user_id = request.form.get('user_id')
        
        email = Email.query.get(email_id)
        user = User.query.get(user_id)
        
        email.sent = True
        db.session.commit()
        
        scheduled_email = Scheduled_Email(email=email, recipient=user, status='Already Scheduled sent to recipient')
        db.session.add(scheduled_email)
        db.session.commit()
        
        return redirect(url_for('view_emails'))
    
    # Define endpoint to delete user
    @app.route('/delete_user', methods=['POST'])
    def delete_user():
        data = request.json
        user_id = data.get('user_id')
        
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"messages": "User successfully deleted"}), 200
        else:
            return jsonify({"error": "User not found and failed to delete"}), 404
        
    # Define endpoint to delete email
    @app.route('/delete_email', methods=['POST'])
    def delete_email():
        data = request.json
        email_id = data.get('email_id')
        
        email = Email.query.get(email_id)
        if email:
            db.session.delete(email)
            db.session.commit()
            return jsonify({"messages": "Email successfully deleted"}), 200
        else:
            return jsonify({"error": "Email not found and failed to delete"}), 404
        
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)