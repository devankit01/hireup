
# Hireup Application 🚀

Welcome to Hireup, a Django-based application designed to streamline the hiring process for both job seekers and recruiters. This powerful platform offers a comprehensive set of features to manage user profiles, job postings, applications, and communications between candidates and recruiters.

## Key Features ✨

1. **User Management:**
   - Users can register, log in, create and update their profiles, and upload resumes. 📄
   
2. **Recruiter Tools:**
   - Recruiters can register, log in, create job postings, track applications, and schedule interviews, all within the platform. 📝
   
3. **Chat Functionality:**
   - Seamless communication between users and recruiters through the integrated chat application. 💬
   
4. **Application Tracking:**
   - Users can monitor the status of their job applications in real-time, keeping them informed every step of the way. 🚀
   
5. **Advanced Job Search & Filters:**
   - Enhanced job search capabilities with filtering options to help users find the perfect job. 🔍

## Installation Guide ⚙️

Follow these steps to set up and run the Hireup application on your local machine:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/hireup.git
   cd hireup
   ```

2. **Install Dependencies:**

   Make sure you have Python 3.9+ installed. Then, create a virtual environment and install the required packages:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Database Migration:**

   Apply the database migrations to set up the database schema:

   ```bash
   python manage.py migrate
   ```

4. **Create a Superuser:**

   To access the Django admin panel and manage the application, create a superuser account:

   ```bash
   python manage.py createsuperuser
   ```

5. **Run the Development Server:**

   Start the Django development server to run the application locally:

   ```bash
   python manage.py runserver
   ```

6. **Access the Application:**

   Once the server is running, you can access the application in your browser at `http://localhost:8000`.

## Usage Instructions 🚀

- **Users:** Register or log in to create a profile, upload your resume, search for jobs, and track your applications.
- **Recruiters:** Register or log in to post jobs, manage applications, and communicate with candidates.
- **Admin Panel:** Access the admin panel at `http://localhost:8000/admin` to manage users, job postings, and other backend data.
