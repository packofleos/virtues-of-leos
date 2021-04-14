## Virtues of Leos
A django webapp for the Leos to compete in doing something good. </br></br>

Admins can create daily tasks, which the user will try to do. For now the tasks are daily and the user gets
point based on their task's amount multiplied by the task's reward. Although, the task have a maximum amount.

## Setting up
1. Clone the repository.
2. Setup virtual environment and activate it then install all the requirements.
3. Configure the settings.py.
    * setup postgres database. Alternatively, comment out postgres and uncomment sqlite3
    * set newly generated SECRET_KET
    * set TIME_ZONE (optional)
4. Migrate the models `python manage.py migrate`
5. Create superuser `python manage.py createsuperuser`

## About
This project is licensed under `GNU Affero General Public License v3`.
