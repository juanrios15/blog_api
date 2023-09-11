# Blog API with Django Rest Framework

Welcome to the Blog API project using Django Rest Framework. This project provides a simple yet comprehensive API for blog management using DRF's ViewSets.

## Installation and Setup

Follow these steps to get the project up and running on your local machine:

### 1. Clone the Repository

Clone this repository to your local machine using `git`:
```
git clone https://github.com/juanrios15/blog_api.git
```

### 2. Set Up a Virtual Environment

Create a virtual environment:
```
python -m venv venv
```
Activate the virtual environment:
- **Windows**:
```
.\venv\Scripts\activate
```
- **MacOS/Linux**:
```
source venv/bin/activate
```

### 3. Install Dependencies

With the virtual environment active, install the project dependencies:
```
pip install -r requirements.txt
```

### 4. Initialize the Database, Create Superuser, and Run the Server

Run the following commands in order to set up the database, create a superuser, and start the development server:
```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Now, you should be able to access the API at `http://127.0.0.1:8000/` and the admin interface at `http://127.0.0.1:8000/admin` using the superuser credentials.

## Obtaining Authentication Token

For user authentication, this project uses Django Rest Framework's Token-based system.

### Steps:

1. **Obtain Token**:
   Use the following `curl` command:

   ```
   curl -X POST \
   -H "Content-Type: application/json" \
   -d '{"username":"your_username","password":"your_password"}' \
   http://localhost:8000/api-token-auth/
   ```

   If successful, you'll get a response similar to:

   ```
   {"token": "YOUR_TOKEN_HERE"}
   ```

2. **Using the Token**:
   For future authenticated API calls, include the token in your request header:

   ```
   Authorization: Token YOUR_TOKEN_HERE
   ```