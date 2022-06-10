# TM-aggregator-with-backend

## Want to use this project?

1. Clone this repository

2. Create and activate a virtual environment:

    ```sh
    $ python3 -m venv env
    ```

3. Install the requirements:

    ```sh
    (env)$ pip install -r requirements.txt
    ```

4. Apply the migrations:

    ```sh
    (env)$ python manage.py makemigrations
    ```
    ```sh
    (env)$ python manage.py migrate
    ```

5. Add your Stripe test secret key, test publishable key, endpoint secret and price API ID to the *secret.py* file (but first create one):

    ```python
    STRIPE_PUBLIC_KEY = '<your test publishable key here>'
    STRIPE_SECRET_KEY = '<your test secret key here>'
    STRIPE_PRICE_ID_PERSONAL = '<your personal price api id here>'
    STRIPE_PRICE_ID_FAMILY = '<your family price api id here>'
    STRIPE_PRICE_ID_BUSINESS = '<your business price api id here>'
    STRIPE_ENDPOINT_SECRET = '<your endpoint secret here>'
    ```
    
6. Run the server:

    ```sh
    (env)$ python manage.py runserver
    ```
