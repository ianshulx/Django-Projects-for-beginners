# Barber Appointment Management System

A Django-based web application for managing barber shop appointments. This system allows customers to book appointments with barbers at different shops, and provides an admin interface for shop management.

## Features

- **Multi-shop Support**: Manage multiple barber shops with different locations and hours
- **Barber Management**: Add and manage barbers with their specialties
- **Service Catalog**: Define services with pricing and duration
- **Online Booking**: Customers can book appointments through an intuitive interface
- **Availability Checking**: Real-time availability checking to prevent double bookings
- **Admin Interface**: Comprehensive Django admin for managing all entities
- **Customer Portal**: Customers can view and manage their appointments
- **Responsive Design**: Mobile-friendly interface using Bootstrap

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the project files**
   ```bash
   # If you have the project files, navigate to the project directory
   cd barberappointment
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser for admin access**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## Initial Setup

After installing and running the application, you'll need to set up your initial data:

1. **Access the Admin Panel**
   - Go to http://127.0.0.1:8000/admin/
   - Log in with your superuser credentials

2. **Add Barber Shops**
   - Navigate to "Barber shops" section
   - Add your shop(s) with name, address, phone, and operating hours

3. **Add Barbers**
   - Navigate to "Barbers" section
   - Add barbers and assign them to shops
   - Include their specialties (e.g., "Haircuts, Beard Trimming, Shaves")

4. **Add Services**
   - Navigate to "Services" section
   - Define services with pricing and duration
   - Assign services to appropriate shops

## Usage

### For Customers

1. **Browse Shops**: View all available barber shops on the home page
2. **Book Appointment**: 
   - Click "Book Appointment" or select a specific shop
   - Choose barber, service, date, and time
   - Fill in contact information
   - Receive confirmation

3. **Manage Appointments**:
   - View existing appointments using email or phone
   - Cancel appointments if needed

### For Administrators

1. **Shop Management**: Add/edit barber shops and their details
2. **Staff Management**: Manage barbers and their information
3. **Service Management**: Define and price services
4. **Appointment Management**: View and manage all appointments
5. **Status Updates**: Update appointment statuses (confirmed, completed, cancelled)

## Project Structure

```
barberappointment/
|-- barberappointment/          # Main Django project directory
|   |-- __init__.py
|   |-- settings.py            # Django settings
|   |-- urls.py               # Main URL configuration
|   |-- wsgi.py               # WSGI configuration
|   |-- asgi.py               # ASGI configuration
|-- appointments/              # Main app directory
|   |-- __init__.py
|   |-- admin.py              # Admin interface configuration
|   |-- apps.py               # App configuration
|   |-- forms.py              # Django forms
|   |-- models.py             # Database models
|   |-- urls.py               # App URL configuration
|   |-- views.py              # View functions
|-- templates/                # HTML templates
|   |-- base.html             # Base template
|   |-- appointments/         # App-specific templates
|       |-- home.html
|       |-- shop_detail.html
|       |-- book_appointment.html
|       |-- confirmation.html
|       |-- my_appointments.html
|       |-- cancel_appointment.html
|-- static/                   # Static files (CSS, JS, images)
|-- manage.py                 # Django management script
|-- requirements.txt          # Python dependencies
|-- README.md                 # This file
```

## Models

### BarberShop
- Shop information (name, address, contact details)
- Operating hours
- Relationships with barbers and services

### Barber
- Barber information and specialties
- Assigned to a specific shop
- Active/inactive status

### Service
- Service details (name, description, duration, price)
- Available at specific shops
- Active/inactive status

### Appointment
- Customer information
- Booking details (shop, barber, service, date, time)
- Status tracking (scheduled, confirmed, completed, cancelled)
- Validation for business rules and availability

## Features in Detail

### Booking System
- **Real-time Availability**: Checks for existing appointments before booking
- **Time Slot Validation**: Ensures appointments don't overlap
- **Business Hours**: Validates appointments within shop operating hours
- **Service Duration**: Prevents bookings that would extend beyond closing time

### Admin Interface
- **Comprehensive Management**: Full CRUD operations for all entities
- **Search and Filter**: Easy navigation through appointments and records
- **Status Management**: Update appointment statuses
- **Bulk Operations**: Efficient management of multiple records

### Customer Experience
- **Intuitive Interface**: Step-by-step booking process
- **Visual Feedback**: Real-time validation and error messages
- **Booking Summary**: Clear confirmation of appointment details
- **Appointment Management**: Easy viewing and cancellation

## Development

### Running Tests
```bash
python manage.py test
```

### Creating New Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

## Security Considerations

- **CSRF Protection**: Enabled by default in Django
- **SQL Injection**: Prevented through Django ORM
- **XSS Protection**: Template auto-escaping enabled
- **Admin Access**: Protected through Django's authentication system

## Deployment

For production deployment, consider:

1. **Environment Variables**: Move sensitive data to environment variables
2. **Database**: Switch from SQLite to PostgreSQL/MySQL
3. **Static Files**: Use a CDN or proper static file serving
4. **HTTPS**: Enable SSL/TLS encryption
5. **Performance**: Implement caching and optimization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and questions:
- Check the Django documentation: https://docs.djangoproject.com/
- Review the code comments and documentation
- Contact the development team

## License

This project is provided as-is for educational and development purposes.

---

**Note**: This is a demonstration project. For production use, additional security measures, testing, and optimization may be required.
