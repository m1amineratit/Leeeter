# Leeeter

A Django REST API project for business and profile management.

## 🚀 Setup Instructions

### 1. Clone the repository

```sh
git clone https://github.com/m1amineratit/Leeeter.git
cd Leeeter
```

### 2. Create and activate a virtual environment

```sh
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```sh
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root with:

```
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### 5. Apply migrations

```sh
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser

```sh
python manage.py createsuperuser
```

### 7. Run the development server

```sh
python manage.py runserver
```

### 8. Access the API

- API root: [http://localhost:8000/api/](http://localhost:8000/api/)
- Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)
- Swagger docs: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

---

## 📝 Notes

- Make sure you have Python 3.8+ installed.
- For Google login, set up OAuth credentials in the Google Cloud Console and add the redirect URI as described in the docs.
- All sensitive settings should be stored in the `.env` file.

---

