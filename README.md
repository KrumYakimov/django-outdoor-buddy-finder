# Outdoor Buddy Finder

**Author: Krum Yakimov**

## Introduction

**Outdoor Buddy Finder** is a social platform that connects outdoor enthusiasts, enabling them to find activity partners for adventures such as hiking, kayaking, skiing, and mountain biking. The platform offers key features such as user profiles, connections, event management, reviews, and more, making it a comprehensive tool for outdoor adventure seekers.

This project was developed as part of my final exam for the **"Django Advanced"** module in the [Python Web](https://softuni.bg/modules/139/python-web/1500) course at **SoftUni**. The goal was to showcase my ability to structure Django applications effectively by applying advanced concepts such as the **Django REST Framework**, **Unit and Integration Testing**, and utilizing the **Django Template Engine** to create clean, maintainable, and reusable code.

## Preview

Here’s a glimpse of the homepage of **Outdoor Buddy Finder**:

![Homepage Screenshot](/static/images/core/home_page_screenshot.png)




---

## Table of Contents
- [Deployment](#deployment)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [License](#license)

---

## Deployment

The **Outdoor Buddy Finder** application is deployed and accessible at:

**[App URL](https://your-deployment-url.com)**

---

## Features

- **User Management**: 
  - Register, login, and manage user profiles.
  - Users can upload profile pictures and contact details.
  
- **Connection System**:
  - Send and manage buddy requests.
  - Accept or decline buddy requests.
  - Disconnect buddies.

- **Event Management**:
  - Create, edit, and join events.
  - View event details and participants.
  - Submit and view event reviews.

- **Reviews**:
  - Leave and manage reviews for events and profiles.
  - Ratings with detailed comments.

- **Notifications**:
  - Welcome Emails: Integrated with AWS SES to send welcome emails when users create an account. This ensures a smooth onboarding experience. 
  - Forgot Password: Configured with SMTP to handle password reset requests securely and efficiently.

---

## Tech Stack

- **Backend**: Python, Django, Django REST Framework
- **Database**: PostgreSQL
- **Testing**: Django Test Framework
- **Third-party Integrations**:
  - AWS SES for email notifications
  - SMTP: Configured for handling password reset functionality using a Gmail third-party email service provider.
  - AWS S3 for image uploads

---

## Setup Instructions

1. **Create a Directory**<br>
   Start by creating a folder for the project:
   ```bash
   mkdir <folder_name>
   cd <folder_name>
   ```
   
2. **Create a virtual environment and activate it:**
   - For macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - For Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Clone the repository:**
   ```bash
    git clone <repository-url>
   ```

5. **Set up PostgreSQL:**
   - Make sure PostgreSQL is installed and running.
   - Create a database for Development environment:
     ```sql
     CREATE DATABASE <database_name>;
     ```
     
6. **Set Up Environment Variables in a `.env` File**  
   Create a `.env` file in the root directory of your project and add the following variables:

   ```plaintext
   # Django settings
   SECRET_KEY=<your_django_secret_key>             # Django secret key from settings.py
   
   # Database configuration
   DB_USER=<your_database_username>                # Database username
   DB_PASSWORD=<your_database_password>            # Database password
   DB_HOST=<your_database_host>                    # Database host (e.g., localhost)
   DB_PORT=<your_database_port>                    # Database port (e.g., 5432 for PostgreSQL)
   DB_NAME=<your_database_name>                    # Main database name
   
   # AWS configuration
   AWS_ACCESS_KEY=<your_aws_access_key>            # AWS access key
   AWS_SECRET=<your_aws_secret_key>                # AWS secret key
   AWS_BUCKET=<your_aws_bucket>                    # S3 bucket name for uploads
   AWS_REGION=<your_aws_region>                    # AWS region (e.g., us-east-1)
   EMAIL_SENDER=<your_aws_email_sender>            # Email sender address for notifications
   
   # SMTP email settings
   EMAIL_HOST=<your_email_host>                    # Email server host
   EMAIL_PORT=<your_email_port>                    # Email server port
   EMAIL_USE_TLS=<your_email_use_tls>              # Use TLS (True/False)
   EMAIL_HOST_USER=<your_email_host_user>          # Email host username
   EMAIL_HOST_PASSWORD=<your_email_host_password>  # Email host password
   DEFAULT_FROM_EMAIL=<your_default_from_email>    # Default sender email address
    ```
   
### Generating a SECRET_KEY for Django

To generate a `SECRET_KEY` for your Django project, you can use Django's built-in functionality. Follow these steps:

1. Open a terminal and navigate to your project directory.

2. Run the Django shell:
   ```bash
   python manage.py shell
   ```

3. Execute the following Python commands:
   ```python
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

4. Copy the generated key, which will look something like this:
   ```
   fQ6yGBkpTc8TzsvuPlpWvK02nvT65dAdBUyXJrQJq45KdZOVbUnm0k3slyMt
   ```

5. Add the key to your `.env` file under the `SECRET_KEY` variable:
   ```plaintext
   SECRET_KEY=fQ6yGBkpTc8TzsvuPlpWvK02nvT65dAdBUyXJrQJq45KdZOVbUnm0k3slyMt
   ```
 

### Running the Application
1. Initialize the database:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

2. Start the Django server:
   ```bash
    python manage.py runserver
    ```
---

## API Endpoints

### Accessing Swagger UI

Once application is running, you can access the Swagger UI at the following URL:

```
http://localhost:8000/api/schema/swagger-ui/
```

### Events
- `POST /events/events` - API endpoint to list all events.

---

## Testing

### Run Tests
To run the test suite:
```bash
python manage.py test
```

### Test Coverage
- **Unit Tests**: Core logic and validations.
- **Integration Tests**: Full workflows (e.g., buddy requests, events and reviews).

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Intellectual Property

The name "**Outdoor Buddy Finder**" and its associated logo and branding are not covered under the MIT License and remain the intellectual property of the author. Any use of these elements without explicit permission is prohibited.


---
