@echo off
cd /d D:\FrameworkDjanggo\project1
call D:\FrameworkDjanggo\env\Scripts\activate.bat
python manage.py runserver 0.0.0.0:8000
pause
