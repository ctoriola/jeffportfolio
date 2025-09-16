from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, TimeField, EmailField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from datetime import datetime, date
import os

# Configure Flask app with proper paths for Vercel
app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static',
           static_url_path='/static')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# Simple in-memory storage for demo (will reset on each deployment)
bookings_storage = []
admin_credentials = {'username': 'admin', 'password': 'admin123'}

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

@app.route('/test-static')
def test_static():
    """Test route to check static file paths"""
    import os
    static_path = os.path.join(app.root_path, '../static')
    static_exists = os.path.exists(static_path)
    css_path = os.path.join(static_path, 'assets/css/main.css')
    css_exists = os.path.exists(css_path)
    
    return f"""
    <h1>Static File Debug</h1>
    <p>App root path: {app.root_path}</p>
    <p>Static folder: {app.static_folder}</p>
    <p>Static URL path: {app.static_url_path}</p>
    <p>Static path exists: {static_exists}</p>
    <p>CSS file exists: {css_exists}</p>
    <p>Static path: {static_path}</p>
    <p>CSS path: {css_path}</p>
    """

@app.route('/book', methods=['GET', 'POST'])
def book():
    form = BookingForm()
    if form.validate_on_submit():
        # Store booking in memory (will be lost on restart)
        booking_data = {
            'id': len(bookings_storage) + 1,
            'name': form.name.data,
            'email': form.email.data,
            'phone': form.phone.data,
            'service_type': form.service_type.data,
            'event_date': form.event_date.data.strftime('%Y-%m-%d'),
            'event_time': form.event_time.data.strftime('%H:%M'),
            'location': form.location.data,
            'message': form.message.data,
            'status': 'pending',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        bookings_storage.append(booking_data)
        
        flash('Your booking request has been submitted successfully! We will contact you within 24 hours.', 'success')
        return redirect(url_for('index'))
    return render_template('booking.html', form=form)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        if (form.username.data == admin_credentials['username'] and 
            form.password.data == admin_credentials['password']):
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    pending_count = len([b for b in bookings_storage if b['status'] == 'pending'])
    confirmed_count = len([b for b in bookings_storage if b['status'] == 'confirmed'])
    
    return render_template('admin/dashboard.html', 
                         bookings=bookings_storage, 
                         pending_count=pending_count,
                         confirmed_count=confirmed_count)

@app.route('/admin/bookings')
def admin_bookings():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    return render_template('admin/bookings.html', bookings=bookings_storage)

@app.route('/admin/booking/update_status', methods=['POST'])
def update_booking_status():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    booking_id = int(request.form.get('booking_id'))
    new_status = request.form.get('status')
    
    # Find and update booking
    for booking in bookings_storage:
        if booking['id'] == booking_id:
            booking['status'] = new_status
            break
    
    flash(f'Booking status updated to {new_status}', 'success')
    return redirect(url_for('admin_bookings'))

@app.route('/admin/content')
def admin_content():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    # Simple content management (static for demo)
    content_items = [
        {'section': 'hero', 'key': 'title', 'value': 'CREATIVE PHOTOGRAPHY'},
        {'section': 'about', 'key': 'title', 'value': 'ABOUT JEFFERY'},
    ]
    return render_template('admin/content.html', content_items=content_items)

@app.route('/admin/content/update', methods=['POST'])
def update_content():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    flash('Content updated successfully (demo mode)', 'success')
    return redirect(url_for('admin_content'))

# For Vercel
if __name__ == '__main__':
    app.run(debug=True)
