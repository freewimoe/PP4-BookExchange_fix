# BookExchange - European School Karlsruhe

A full-stack Django web application for exchanging used schoolbooks within the European School Karlsruhe community.

![BookExchange Homepage](screenshots/homepage.png)

## Live Application
🔗 **Deployed on Heroku:** [https://pp4-bookexchange-app-a3060fbcdcb6.herokuapp.com/](https://pp4-bookexchange-app-a3060fbcdcb6.herokuapp.com/)

## Project Overview

BookExchange is a comprehensive book trading platform designed specifically for the European School Karlsruhe. Students can browse the official school booklist (470+ books), create offers for their used books, and connect with other students to buy/sell textbooks.

## Technologies Used

### Backend
- **Python 3.12** - Core programming language
- **Django 4.2.23** - Web framework
- **PostgreSQL** - Production database (Heroku)
- **SQLite** - Development database

### Frontend
- **HTML5** - Structure
- **CSS3** & **Bootstrap 5** - Styling and responsive design
- **JavaScript** - Interactive elements

### Deployment & Tools
- **Heroku** - Cloud platform deployment
- **WhiteNoise** - Static file serving
- **Gunicorn** - WSGI HTTP Server
- **Git** - Version control
- **VS Code** - Development environment

### Dependencies
```
Django==4.2.23
psycopg2-binary==2.9.10
whitenoise==6.9.0
gunicorn==22.0.0
pillow==11.2.1
python-dotenv==1.1.0
```

## User Stories

### As a Student:
- **Browse Books**: I want to browse the official school booklist to see what books are available
- **Search & Filter**: I want to filter books by section (DE/EN/FR), class (S1-S7), and subject
- **View Details**: I want to see detailed information about each book including ISBN, publisher, and edition
- **Create Offers**: I want to offer my used books for sale with condition and price information
- **Contact Sellers**: I want to contact other students who are selling books I need
- **Manage My Offers**: I want to view, edit, and delete my own book offers

### As a School Administrator:
- **Manage Booklist**: I want to maintain the official school booklist through the admin interface
- **Monitor Activity**: I want to see statistics about book offers and user activity

## Features

### Implemented Features

#### 📚 Official School Booklist
- **470+ Real School Books** imported from European School Karlsruhe official list
- **Structured by Sections**: German (DE), English (EN), French (FR)
- **Class Organization**: S1DE, S2EN, S3FR, etc.
- **Complete Book Information**: Title, Author, ISBN, Publisher, Edition, Subject

#### 🔍 Advanced Search & Filtering
- **Text Search**: Search by title, author, or subject
- **Section Filter**: Filter by language section (DE/EN/FR)
- **Class Filter**: Filter by school class (S1-S7)
- **Subject Filter**: Filter by academic subject
- **Pagination**: 20 books per page for performance

#### 💰 Student Offers System
- **Offer Creation**: Students can create offers for any book from the official list
- **Condition Rating**: New, Used, Worn, Poor condition options
- **Price Setting**: Flexible pricing in Euros
- **Contact Information**: Email and optional phone contact
- **Photo Upload**: Optional book condition photos
- **Additional Notes**: Extra condition details

#### 👤 User Management
- **Django Authentication**: Secure login/logout system
- **User Registration**: New student account creation
- **Offer Management**: Users can view, edit, and delete their own offers
- **Contact Protection**: Email addresses only shown to interested buyers

#### 📱 Responsive Design
- **Mobile-First**: Works on phones, tablets, and desktops
- **Bootstrap 5**: Modern, professional styling
- **Card-Based Layout**: Clean, organized presentation
- **Navigation**: Intuitive menu structure

#### 🛡️ Admin Interface
- **Django Admin**: Full administrative control
- **Book Management**: Add, edit, delete school books
- **User Management**: Monitor user accounts and offers
- **Data Import**: CSV import functionality for booklist updates

### Future Features
- **Wishlist System**: Students can mark books they want to buy
- **Rating System**: Rate transactions and build trust
- **Notification System**: Email alerts for new offers
- **Advanced Messaging**: In-app messaging between users
- **Price Analytics**: Historical price tracking and suggestions

## Database Schema

### Models

#### SchoolBook
- Official school booklist entries
- Fields: title, author, isbn, edition, publisher, school_class, subject, section, notes

#### StudentOffer  
- Student offers for school books
- Fields: school_book (FK), seller (FK), condition, price, contact_email, contact_phone, image, additional_notes

#### User (Django built-in)
- Student accounts and authentication

## Testing

### Manual Testing

#### Functionality Testing
✅ **User Registration/Login**: Successfully create accounts and authenticate  
✅ **Browse Books**: View all 470+ school books with pagination  
✅ **Search & Filter**: All filter combinations work correctly  
✅ **Create Offers**: Successfully create offers with all form fields  
✅ **Edit/Delete Offers**: Users can modify their own offers  
✅ **Contact Sellers**: Email links work correctly  
✅ **Admin Interface**: Full CRUD operations on all models  

#### Browser Testing
✅ **Chrome**: Full functionality  
✅ **Firefox**: Full functionality  
✅ **Safari**: Full functionality  
✅ **Mobile Chrome**: Responsive design works  

#### Device Testing
✅ **Desktop**: 1920x1080 - Perfect layout  
✅ **Tablet**: 768px - Responsive grid  
✅ **Mobile**: 375px - Single column layout  

### Automated Testing
```python
# Example test case
def test_school_book_list_view(self):
    response = self.client.get('/books/')
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'European School Karlsruhe')
```

### Code Validation
- **HTML**: W3C Markup Validator - No errors
- **CSS**: W3C CSS Validator - No errors  
- **Python**: PEP8 compliant code
- **JavaScript**: ESLint - No errors

## Deployment

### Heroku Deployment Process

1. **Create Heroku App**
```bash
heroku create pp4-bookexchange-app
```

2. **Configure Environment Variables**
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
```

3. **Add PostgreSQL Database**
```bash
heroku addons:create heroku-postgresql:mini
```

4. **Deploy Application**
```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py collectstatic --noinput
```

5. **Import School Booklist**
```bash
heroku run python manage.py import_books BOOKLIST_2023_2024.csv
```

### Environment Configuration

#### Production (Heroku)
- PostgreSQL database
- WhiteNoise for static files
- Gunicorn WSGI server
- Debug=False

#### Development (Local)
- SQLite database
- Django development server
- Debug=True

## Local Installation

### Prerequisites
- Python 3.12+
- Git

### Setup Instructions

1. **Clone Repository**
```bash
git clone https://github.com/freewimoe/PP4-BookExchange.git
cd PP4-BookExchange
```

2. **Create Virtual Environment**
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment**
```bash
# Create .env file
DEBUG=True
SECRET_KEY=your-local-secret-key
```

5. **Database Setup**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

6. **Import School Books**
```bash
python manage.py import_books BOOKLIST_2023_2024_cleaned_utf8_comma.csv
```

7. **Run Development Server**
```bash
python manage.py runserver
```

8. **Access Application**
- Main site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Screenshots

### Homepage
![Homepage with Statistics](screenshots/homepage.png)
*Homepage showing book statistics and navigation*

### Book List
![School Book List](screenshots/book-list.png)
*Browse official European School Karlsruhe booklist*

### Book Details
![Book Detail View](screenshots/book-detail.png)
*Detailed book information with available offers*

### Create Offer
![Create Offer Form](screenshots/create-offer.png)
*Form to create new book offers*

### Admin Interface
![Django Admin](screenshots/admin.png)
*Admin interface for managing books and offers*

## Repository Structure
```
PP4-BookExchange/
├── bookexchange/           # Django project settings
├── books/                  # Main application
│   ├── migrations/         # Database migrations
│   ├── templates/books/    # HTML templates
│   ├── management/         # Custom commands
│   └── models.py          # Data models
├── static/                # Static files (CSS, JS, images)
├── media/                 # User uploaded files
├── requirements.txt       # Python dependencies
├── manage.py             # Django management script
└── README.md             # This file
```

## Learning Outcomes Achieved

### LO1 - Algorithm Implementation
✅ **CSV Import Algorithm**: Custom management command processes 716 book records with data cleaning and validation  
✅ **Search Algorithm**: Multi-field search with filters and pagination  
✅ **Price Sorting**: Offers sorted by price for optimal user experience  

### LO2 - Data Source Integration  
✅ **Official School Booklist**: Real CSV data from European School Karlsruhe imported into PostgreSQL  
✅ **Database Models**: SchoolBook and StudentOffer models with proper relationships  
✅ **Admin Interface**: Full CRUD operations through Django admin  

### LO3 - Full Stack Django Application
✅ **Views**: Class-based and function-based views for all operations  
✅ **Templates**: Responsive HTML templates with Bootstrap 5  
✅ **Forms**: Django forms with validation for user input  
✅ **Authentication**: Complete user registration and login system  
✅ **Testing**: Manual testing procedures documented  

### LO4 - Deployment & Documentation
✅ **Heroku Deployment**: Live application with PostgreSQL database  
✅ **Comprehensive README**: Complete documentation with setup instructions  
✅ **Screenshots**: Visual documentation of key features  
✅ **Repository**: Clean, organized code structure  

## Credits

### Data Source
- **European School Karlsruhe**: Official 2023-2024 booklist (470+ books)

### Technologies
- **Django Documentation**: Framework guidance
- **Bootstrap 5**: UI components and responsive design
- **Heroku**: Cloud platform deployment

### Development
- **Code Institute**: Educational support and project requirements
- **MDN Web Docs**: HTML, CSS, and JavaScript reference

---

**Project completed as part of Code Institute Full Stack Software Development Diploma**  
**Student: Friedrich-Wilhelm Moeller**  
**Submission Date: June 2025**