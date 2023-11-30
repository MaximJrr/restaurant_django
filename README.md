# Restaurant
*Access to website:* **-------------**
---
### This website allows users to order dishes, book a table

## *Tools*:
*Python 3.10*

*Django*

*Django REST framework*

*Docker*

*Postgres*

*Redis*

*Celery*

## **Installation**
1. Clone the repository:
```python
git clone https://github.com/MaximJrr/restaurant_django.git
```

2. Create a virtual environment and activate it:
```python
python3 -m venv venv
source venv/bin/activate
```

 3. Install dependencies from the file **requirements.txt**:
```python
pip install --upgrade pip
pip install -r requirements.txt
```

4. Run project dependencies, migrations, fill the database with the fixture data:
```python
./manage.py migrate
./manage.py loaddata <path_to_fixture_files>
./manage.py runserver 
```

5. Run Redis Server:
```python
redis-server
```

6. Run Celery:
```python
celery -A restaurant worker --loglevel=INFO
```