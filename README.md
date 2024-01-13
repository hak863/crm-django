# crm-django

# Contact Management System (CRM)

Welcome to the Contact Management System (CRM) project! This system is designed to help you efficiently manage your contacts and customer relations. Below, you'll find an overview of the project's files, features, and technologies used.

## Files

- `README.md`: This file provides an introduction and overview of the project.
- `app.py`: The main application file that contains the logic for managing contacts and customer relations.
- `models.py`: Defines the database models for storing contact information.
- `views.py`: Contains the views and routes for handling user requests.
- `templates/`: This directory contains the HTML templates for rendering the user interface.
- `static/`: Stores static files such as CSS stylesheets and images.

## Leads App

### Files

- `migrations/`: Database migration files for the leads app.
- `templates/leads/`: HTML templates for rendering the leads app interface.
- `__init__.py`
- `admin.py`: Admin configurations for the leads app.
- `apps.py`: App configuration for the leads app.
- `forms.py`: Forms for handling lead-related data.
- `models.py`: Database models for storing lead information.
- `tests.py`: Unit tests for the leads app.
- `urls.py`: URL patterns for the leads app.
- `views.py`: Contains views for handling lead-related requests.

### Features

- **Lead Management:** Create, view, update, and delete leads. Organizes leads using categories.
- **Category Management:** Organizes and categorizes leads using a category model.
- **Assign Agent:** Allows assigning agents to leads for efficient management.
- **Follow-up:** Enables tracking and scheduling follow-up activities for leads.

## Agents App

### Files

- `migrations/`: Database migration files for the agents app.
- `templates/agents/`: HTML templates for rendering the agents app interface.
- `__init__.py`
- `admin.py`: Admin configurations for the agents app.
- `apps.py`: App configuration for the agents app.
- `forms.py`: Forms for handling agent-related data.
- `models.py`: Database models for storing agent information.
- `tests.py`: Unit tests for the agents app.
- `urls.py`: URL patterns for the agents app.
- `views.py`: Contains views for handling agent-related requests.

### Features

- **Agent Management:** Create, view, update, and delete agents. Defines different user types.
- **User Authentication:** Implements custom user models for authentication. Manages user sessions and permissions.
- **Email Functionality:** Sends emails for various purposes, such as notifications and password reset.
- **Password Reset:** Enables users to reset their passwords.
- **Styling and UI:** Uses TailwindCSS for styling the user interface.
- **Email Sending with Mailgun:** Configures Mailgun for sending emails.

## Technologies Used

- Python: The programming language used for the backend logic.
- Django: A powerful web framework for building web applications.
- TailwindCSS: A utility-first CSS framework for styling the user interface.
- Mailgun: An email service provider used for sending emails.