## Pinterest Clone

This project is designed to be a simple replication of the pinterest idea, made as a coding challenge for interview.

## Features

- Allows users to post images, with titles, descriptions and tags.
- Users can register and login.
- Users can like each other posts.
- Users can search for images by title, tags and author username.
- Users can order pins by most recent or most liked.
- Pins are paginated.
- Unit tests for the main endpoints.

To run this, you will need the following technologies installed: 

- Python 3.9.4
- Django 4.2.13

1. Clone the repository:
    ```bash
    git clone https://github.com/NatanFS/PinterestClone
    cd pinterestlike
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply the migrations:
    ```bash
    cd src/
    pytho3 manage.py migrate
    ```

5. Run the development server:
    ```bash
    python3 manage.py runserver
    ```

5. Run the unit tests:
    ```bash
    python3 manage.py tests
    ```

Now, your backend project is running! :) 




 
