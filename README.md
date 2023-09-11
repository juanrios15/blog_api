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
   {"token": "YOUR_TOKEN"}
   ```

2. **Using the Token**:
   For future authenticated API calls, include the token in your request header:

   ```
   curl -X GET \
   -H "Authorization: Token YOUR_TOKEN" \
   http://localhost:8000/blog/posts
   ```

## Posts Endpoint

**Endpoint**: `/blog/posts/`

This endpoint provides CRUD operations for blog posts.

### Query Example:

Here's an example using `curl` to filter posts by title, created time, and a specific username:

```
curl -X GET \
-H "Authorization: Token YOUR_TOKEN" \
"http://localhost:8000/blog/posts/?title__icontains=example&created_time__gte=2023-01-01&user__username__icontains=john"
```

### Permissions:

- **View Posts**: Any user can view posts with `is_active=True` via "list" and "retrieve" actions. Superusers can view all posts.
  
- **Create/Update/Delete Posts**: Only the owner of a post or a superuser can update, partially update or delete the post. When creating a post, only superusers will have their posts set to `is_active=True` by default. Other users will need their posts approved to become active.

- **Approve Posts**: Only superusers can approve posts, using the "approve_post" action.

- **Other Actions**: Admin users have permission for all other actions not explicitly mentioned above.

### Approve Post Endpoint:

**Endpoint**: `/blog/posts/{id}/approve_post/`

This endpoint allows superusers to approve a post, setting its `is_active` status to `True`. 

Example with `curl`:

```
curl -X POST \
-H "Authorization: Token YOUR_TOKEN" \
"http://localhost:8000/blog/posts/1/approve_post/"
```

## Comments Endpoint

**Endpoint**: `/blog/comments/`

This endpoint provides CRUD operations for comments associated with blog posts.

### Query Example:

Here's how to use `curl` to filter comments by their text, post ID, creation date, and user:

```
curl -X GET \
-H "Authorization: Token YOUR_TOKEN" \
"http://localhost:8000/blog/comments/?comment_text__icontains=example&created_time__gte=2023-01-01&post__in=1,2,3&user__exact=1"
```

### Permissions:

- **Update Comments**: Only the owner of a comment can update or partially update the comment.
  
- **Delete Comments**: Either the owner of the comment or staff users can delete a comment.

- **View Comments**: Any user can view comments marked with `is_active=True`. Superusers have the privilege to view all comments, including those with `is_active=False`.

- **All Other Actions**: Any user is permitted for all other actions not explicitly mentioned.

## Likes Endpoint

**Endpoint**: `/blog/likes/`

The likes endpoint allows users to like various entities within the application.

### Features:

1. **Flexibility to Like Various Entities**: A user can give a like to any entity such as Posts, Comments, or any other model. This flexibility is achieved using Django's `GenericForeignKey`.

2. **Unique Constraint**: A user can only give one like per entity, ensuring that likes are unique based on the user, content type, and object ID.

3. **Permissions**:
   - **Listing, Retrieving, and Creating Likes**: Any user can perform these actions.
   - **Updating and Deleting Likes**: Only the owner of a like or a staff member can perform these actions.
   - **Viewing Likes**: All users can view likes that are marked with `is_active=True`. Superusers can view all likes, including those with `is_active=False`.

### Example - Creating a Like using `curl`:

To create a like for a post with ID 1, you can use the following `curl` command:

```
curl -X POST \
-H "Authorization: Token YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{"name": "John Doe", "email": "johndoe@example.com", "user": 1, "liked": true, "content_type": POST_CONTENT_TYPE_ID, "object_id": 1, "is_active": true}' \
"http://localhost:8000/blog/likes/"
```

Replace `POST_CONTENT_TYPE_ID` with the appropriate content type ID for the post model. The `content_type` field represents the model (or entity) you are liking, and `object_id` is the ID of the specific instance of that model.

### Retrieving Content Types

To identify which models you can give a "like", you'll need to fetch the `ContentType` IDs. The superuser can access this information through the following endpoint:

**Endpoint**: `/blog/contenttypes/` GET method