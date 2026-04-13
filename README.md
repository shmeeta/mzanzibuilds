#MZANSIBUILDS

### Who It’s For
* **Individual Developers:** Looking for accountability and a public log of their work.
* **Collaborators:** Looking to join existing projects by "raising a hand."
* **Tech Communities:** People who value transparency and learning from real-time builds.

---

##  Key Features
* **Developer Profiles:** Secure account management for individual creators.
* **Project Tracking:** Create and manage entries, specifying current stages and support requirements.
* **Live Collaboration Feed:** Real-time stream of community activity where users can comment or request to join.
* **Milestone System:** Log continuous progress updates to keep followers informed.
* **The Celebration Wall:** A hall-of-fame dedicated to developers who successfully ship their projects.

---

## Tech Stack
* **Framework:** Django (Python)
* **Frontend:** Django Templates
* **Styling:** Bootstrap (Palette: Green, White, and Black)
* **Database:** SQLite (Default) / PostgreSQL

---

## 💻 Installation & Setup

Follow these steps to get your local development environment up and running.

### 1. Clone the Repository
```bash
git clone <your-repo-link>
cd <project-folder-name>
``` 

### 2. Envionment Setup 
Create a virtual environment to keep your project dependencies isolated. 
```bash
python -m venv venv
```

### 3. Activate it:

```bash
Windows: venv\Scripts\activate

Mac/Linux: source venv/bin/activate
```
### 4. Install Dependencies 

```bash
pip install -r requirements.txt
```

### 5. Environment Configuration
Create a .env file in the root directory. This keeps your sensitive credentials secure and out of version control.
```bash
DEBUG=True
SECRET_KEY=your_django_secret_key_here
# Database Config (if using PostgreSQL/MySQL)
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
```
### 6.Database Initialization 

```bash
python manage.py makemigrations
python manage.py migrate
```


### 7.Launch the Application

```bash
python manage.py runserver
```
Once started, you can view the platform at:

👉 http://127.0.0.1:8000/


## Deployment and Availability: 
Deployed using render and available for viewing at: https://mzansi-builds-el3r.onrender.com/
