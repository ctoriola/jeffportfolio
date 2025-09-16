# Jeffery Chinda Photography Portfolio

A professional photography portfolio website with booking system and admin panel built with Flask.

## Features

### Public Website
- **Modern Portfolio Design**: Responsive photography portfolio showcasing Jeffery's work
- **Booking System**: Integrated booking form in the hero section for easy client inquiries
- **Service Showcase**: Display of photography services (Portrait, Event, Wedding, Commercial)
- **Professional Layout**: Clean, modern design optimized for photography portfolios

### Admin Panel
- **Booking Management**: View, update, and manage client booking requests
- **Content Management**: Edit website content including titles, descriptions, and text
- **Dashboard**: Overview of bookings, statistics, and recent activity
- **Secure Authentication**: Password-protected admin access

### Booking System
- **Real-time Form**: Instant booking requests with form validation
- **Service Selection**: Choose from different photography packages with pricing
- **Email Integration**: Direct email links for client communication
- **Status Tracking**: Pending, Confirmed, Completed, Cancelled status options

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or Download the Project**
   ```bash
   cd c:\Users\TOG-M\Downloads\jeff
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python app.py
   ```

4. **Access the Website**
   - Main website: http://localhost:5000
   - Admin login: http://localhost:5000/admin/login
   - Admin dashboard: http://localhost:5000/admin

## Default Admin Credentials

- **Username**: admin
- **Password**: admin123

⚠️ **Important**: Change these credentials in production!

## Usage

### For Clients
1. Visit the main website at http://localhost:5000
2. Use the booking form in the hero section to request a photography session
3. Fill out all required fields including service type, date, and location
4. Submit the form and receive confirmation

### For Admin (Jeffery)
1. Go to http://localhost:5000/admin/login
2. Login with admin credentials
3. **Dashboard**: View booking statistics and recent requests
4. **Bookings**: Manage all booking requests, update status, contact clients
5. **Content Management**: Edit website text and content

## File Structure

```
jeff/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── index.html        # Main portfolio page
│   ├── booking.html      # Booking form page
│   ├── base.html         # Base template
│   └── admin/            # Admin templates
│       ├── login.html    # Admin login
│       ├── dashboard.html # Admin dashboard
│       ├── bookings.html # Booking management
│       └── content.html  # Content management
└── static/               # Static files (CSS, JS, Images)
    └── assets/           # Original template assets
        ├── css/          # Stylesheets
        ├── js/           # JavaScript files
        └── img/          # Images
```

## Database

The application uses SQLite database (`photography_portfolio.db`) with the following tables:

- **bookings**: Store client booking requests
- **admin**: Admin user accounts
- **content**: Editable website content

Database is automatically created on first run.

## Customization

### Changing Images
1. Replace images in `static/assets/img/` directory
2. Update image references in templates if needed

### Modifying Content
1. Use the admin panel Content Management section
2. Or directly edit templates in the `templates/` folder

### Adding New Services
1. Update the service options in `app.py` (BookingForm class)
2. Update pricing in templates and booking form

### Styling Changes
1. Modify CSS in `static/assets/css/main.css`
2. Add custom styles in template `<style>` sections

## Production Deployment

### Security Considerations
1. Change the SECRET_KEY in `app.py`
2. Change default admin credentials
3. Use a production database (PostgreSQL, MySQL)
4. Enable HTTPS
5. Set up proper error handling and logging

### Environment Variables
Consider using environment variables for:
- SECRET_KEY
- DATABASE_URL
- ADMIN_USERNAME
- ADMIN_PASSWORD

### Hosting Options
- **Heroku**: Easy deployment with git
- **DigitalOcean**: VPS hosting
- **AWS**: Elastic Beanstalk or EC2
- **PythonAnywhere**: Simple Python hosting

## Support

For technical support or customization requests, please contact the developer.

## License

This project is for Jeffery Chinda Photography. All rights reserved.
