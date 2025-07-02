# Leeeter API

A modern Django REST Framework API for business pages, built with secure **Google OAuth2 authentication only**.

---

## 🚀 Features

- **Google-only authentication:** No basic or password login, only Google OAuth2.
- **RESTful API:** Clean endpoints for business, client, and page management.
- **Secure:** JWT authentication, no session or basic auth endpoints exposed.
- **Scalable:** Modular code with clear separation of models, serializers, and views.
- **Browsable API:** Swagger and Redoc documentation included.

---

## 🔒 Authentication

**Only Google OAuth2 is supported.**  
Users must log in with their Google account to access any protected endpoints.

### How it works

1. **Frontend:** Obtain a Google OAuth2 access token (using Google Sign-In).
2. **Backend:**  
   Send a POST request to:

   ```
   POST /api/auth/google/login/
   Content-Type: application/json

   {
     "access_token": "GOOGLE_ACCESS_TOKEN"
   }
   ```

3. **Response:**  
   You receive a JWT token and user info for authenticated API access.

---

## ⚙️ Setup Instructions

1. **Clone the repo and install dependencies:**
    ```sh
    git clone https://github.com/m1amineratit/Leeeter.git
    cd Leeeter
    pip install -r requirements.txt
    ```

2. **Create and activate a virtual environment**

```sh
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

3. **Configure Google OAuth2:**
    - Create OAuth credentials at [Google Developer Console](https://console.developers.google.com/).
    - Set the **Authorized redirect URI** to:
      ```
      http://localhost:8000/api/auth/google/login/callback/
      ```
    - Add your Google client ID and secret to your environment or `settings.py`:
      ```python
      SOCIALACCOUNT_PROVIDERS = {
          'google': {
              'SCOPE': ['profile', 'email'],
              'AUTH_PARAMS': {'access_type': 'online'},
              'APP': {
                  'client_id': '<your-client-id>',
                  'secret': '<your-client-secret>',
                  'key': ''
              }
          }
      }
      ```

4. **Run migrations:**
    ```sh
    python manage.py migrate
    ```

5. **Start the server:**
    ```sh
    python manage.py runserver
    ```

6. **Access the API docs:**
    - Swagger: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
    - Redoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

---

## 🧪 Testing Google Login

You can test Google login using Postman or the browsable API:

- **Endpoint:** `POST /api/auth/google/login/`
- **Body:**
    ```json
    {
      "access_token": "your_google_access_token"
    }
    ```

---

## 📁 Project Structure

- `core/` — Main app with models, serializers, and views.
- `leeeter/` — Project settings and URLs.
- `requirements.txt` — Python dependencies.

---

## 📝 Notes

- **No registration, password reset, or basic login endpoints are exposed.**
- **All authentication is handled via Google OAuth2.**
- **Admin access is available at `/admin/` for superusers.**

---

## 🙋‍♂️ Questions?

If you have any questions or need a demo frontend, please let me know!

---

**Thank you for reviewing this project!**

