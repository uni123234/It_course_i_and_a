
# IT Course Management System

## Опис проекту

Цей проект є системою управління курсами IT, яка дозволяє користувачам легко знаходити, реєструватися та відстежувати прогрес у різних курсах. Система створена для полегшення навчання та забезпечення доступу до ресурсів для студентів та викладачів.

## Функціональні можливості

- **Реєстрація та аутентифікація:** Користувачі можуть реєструватися та входити в систему, щоб отримати доступ до особистих налаштувань та курсів.
- **Управління курсами:** Викладачі можуть створювати та редагувати курси, додавати матеріали та завдання.
- **Взаємодія зі студентами:** Студенти можуть задавати питання, залишати відгуки та спілкуватися з викладачами.
- **Моніторинг прогресу:** Користувачі можуть відстежувати свій прогрес у курсах і отримувати сповіщення про нові матеріали та завдання.

## Технології

- **Backend:** Django Rest Framework для створення API.
- **Frontend:** React для побудови інтерактивного інтерфейсу користувача.
- **База даних:** PostgreSQL для зберігання даних про користувачів та курси.

## Як запустити проект

### Спосіб 1: Запуск без Docker

1. **Створіть віртуальне середовище:**
   ```bash
   python -m venv venv
   ```

2. **Активуйте віртуальне середовище:**
   ```bash
   source venv/bin/activate  # Для Linux/Mac
   venv\Scripts\activate     # Для Windows
   ```

3. **Перейдіть до папки з бекендом:**
   ```bash
   cd backend/it_course_backend
   ```

4. **Встановіть залежності:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Створіть суперкористувача (superuser):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Запустіть сервер:**
   ```bash
   python manage.py runserver
   ```

7. **Перейдіть до фронтенду:**
   ```bash
   cd frontend
   ```

8. **Встановіть залежності:**
   ```bash
   npm install
   ```

9. **Запустіть фронтенд:**
   ```bash
   npm run dev
   ```

### Спосіб 2: Запуск з Docker

1. **Переконайтеся, що Docker встановлений на вашій машині.**

2. **Запустіть Docker-команди для створення контейнерів:**
   ```bash
   docker-compose up --build
   ```

3. **Створіть суперкористувача (superuser) в Docker-контейнері:**
   ```bash
   docker exec -it <container_name> python manage.py createsuperuser
   ```

   Замість `<container_name>` використовуйте ім'я контейнера вашого бекенду (перевірте його командою `docker ps`).

### Спосіб 3: Очищення Docker

Якщо вам потрібно очистити Docker, щоб звільнити місце:

1. **Видалити всі контейнери:**
   ```bash
   docker rm $(docker ps -aq)
   ```

2. **Видалити всі образи:**
   ```bash
   docker rmi $(docker images -q)
   ```

## Налаштування середовища (Environment Variables)

Створіть файл `.env` у кореневій папці проекту з наступним вмістом:

```
SECRET_KEY=your_token
DEBUG=True
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_PORT=5432
ALLOWED_HOSTS=127.0.0.1
AUTH_COOKIE_SECURE=True
ACCESS_TOKEN_LIFETIME=3600
REFRESH_TOKEN_LIFETIME=86400
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

Зверніть увагу, що потрібно замінити `your_token`, `your_db_name`, `your_db_user`, `your_db_password`, `your_google_client_id` та `your_google_client_secret` на ваші власні значення.


# IT Course Management System

## Project Description

This project is an IT course management system that allows users to easily find, register, and track progress in various courses. The system is designed to facilitate learning and provide access to resources for students and instructors.

## Features

- **Registration and Authentication:** Users can sign up and log in to access personal settings and courses.
- **Course Management:** Instructors can create and edit courses, add materials, and assignments.
- **Student Interaction:** Students can ask questions, leave feedback, and communicate with instructors.
- **Progress Tracking:** Users can track their progress in courses and receive notifications about new materials and assignments.

## Technologies

- **Backend:** Django Rest Framework for API creation.
- **Frontend:** React for building an interactive user interface.
- **Database:** PostgreSQL for storing user and course data.

## How to Run the Project

### Method 1: Run Without Docker

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```

3. **Navigate to the backend folder:**
   ```bash
   cd backend/it_course_backend
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the server:**
   ```bash
   python manage.py runserver
   ```

7. **Navigate to the frontend:**
   ```bash
   cd frontend
   ```

8. **Install dependencies:**
   ```bash
   npm install
   ```

9. **Run the frontend:**
   ```bash
   npm run dev
   ```

### Method 2: Run with Docker

1. **Make sure Docker is installed on your machine.**

2. **Run Docker commands to create containers:**
   ```bash
   docker-compose up --build
   ```

3. **Create a superuser in the Docker container:**
   ```bash
   docker exec -it <container_name> python manage.py createsuperuser
   ```

   Replace `<container_name>` with the name of your backend container (check it with `docker ps` command).

### Method 3: Clean Up Docker

If you need to clean up Docker to free up space:

1. **Remove all containers:**
   ```bash
   docker rm $(docker ps -aq)
   ```

2. **Remove all images:**
   ```bash
   docker rmi $(docker images -q)
   ```

## Environment Variables

Create a `.env` file in the root of the project with the following content:

```
SECRET_KEY=your_token
DEBUG=True
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_PORT=5432
ALLOWED_HOSTS=127.0.0.1
AUTH_COOKIE_SECURE=True
ACCESS_TOKEN_LIFETIME=3600
REFRESH_TOKEN_LIFETIME=86400
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

Make sure to replace `your_token`, `your_db_name`, `your_db_user`, `your_db_password`, `your_google_client_id`, and `your_google_client_secret` with your own values.
