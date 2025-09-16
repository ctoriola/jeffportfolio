from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, TimeField, EmailField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///photography_portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    event_time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(50), nullable=False)
    key = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

# Forms
class BookingForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    service_type = SelectField('Service Type', choices=[
        ('portrait', 'Portrait Photography - $299'),
        ('event', 'Event Photography - $799'),
        ('wedding', 'Wedding Photography - $1,999'),
        ('commercial', 'Commercial Photography - Custom Quote')
    ], validators=[DataRequired()])
    event_date = DateField('Event Date', validators=[DataRequired()])
    event_time = TimeField('Event Time', validators=[DataRequired()])
    location = StringField('Event Location', validators=[DataRequired(), Length(min=5, max=200)])
    message = TextAreaField('Additional Details')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    form = BookingForm()
    if form.validate_on_submit():
        booking = Booking(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            service_type=form.service_type.data,
            event_date=form.event_date.data,
            event_time=form.event_time.data,
            location=form.location.data,
            message=form.message.data
        )
        db.session.add(booking)
        db.session.commit()
        flash('Your booking request has been submitted successfully! We will contact you within 24 hours.', 'success')
        return redirect(url_for('index'))
    return render_template('booking.html', form=form)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and check_password_hash(admin.password_hash, form.password.data):
            session['admin_logged_in'] = True
            session['admin_id'] = admin.id
            return redirect(url_for('admin_dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_id', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    pending_count = Booking.query.filter_by(status='pending').count()
    confirmed_count = Booking.query.filter_by(status='confirmed').count()
    
    return render_template('admin/dashboard.html', 
                         bookings=bookings, 
                         pending_count=pending_count,
                         confirmed_count=confirmed_count)

@app.route('/admin/bookings')
def admin_bookings():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return render_template('admin/bookings.html', bookings=bookings)

@app.route('/admin/booking/<int:booking_id>/update_status', methods=['POST'])
def update_booking_status():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    booking_id = request.form.get('booking_id')
    new_status = request.form.get('status')
    
    booking = Booking.query.get_or_404(booking_id)
    booking.status = new_status
    db.session.commit()
    
    flash(f'Booking status updated to {new_status}', 'success')
    return redirect(url_for('admin_bookings'))

@app.route('/admin/content')
def admin_content():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    content_items = Content.query.all()
    return render_template('admin/content.html', content_items=content_items)

@app.route('/admin/content/update', methods=['POST'])
def update_content():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    section = request.form.get('section')
    key = request.form.get('key')
    value = request.form.get('value')
    
    content = Content.query.filter_by(section=section, key=key).first()
    if content:
        content.value = value
        content.updated_at = datetime.utcnow()
    else:
        content = Content(section=section, key=key, value=value)
        db.session.add(content)
    
    db.session.commit()
    flash('Content updated successfully', 'success')
    return redirect(url_for('admin_content'))

def init_db():
    """Initialize the database with default admin user and content"""
    db.create_all()
    
    # Create default admin if not exists
    if not Admin.query.first():
        admin = Admin(
            username='admin',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin)
    
    # Add default content
    default_content = [
        ('hero', 'title', 'CREATIVE PHOTOGRAPHY'),
        ('hero', 'subtitle', 'Capturing life\'s most precious moments through artistic vision'),
        ('about', 'title', 'ABOUT JEFFERY'),
        ('about', 'description', 'Jeffery Chinda is a passionate photographer with an eye for detail and a commitment to excellence.'),
    ]
    
    for section, key, value in default_content:
        if not Content.query.filter_by(section=section, key=key).first():
            content = Content(section=section, key=key, value=value)
            db.session.add(content)
    
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
