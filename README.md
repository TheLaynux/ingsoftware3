# ingsoftware3
crear entorno virtual

python -m venv venv

activar entorno virtual

venv/Scripts/activate

en caso de error ejecutar

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

venv/Scripts/activate.ps1

luego
 pip install -r requirements.txt
 python manage.py createsuperuser

 e iniciar servidor

 python manage.py runserver
 