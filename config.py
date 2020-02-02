import os
DEBUG=True
SECRET_KEY=os.environ.get('SECRET_KEY') or 'vikrant.deshpande09876@gmail.com-ismyemail'
UPLOAD_DIR=os.environ.get('UPLOAD_DIR') or 'C:\\Users\\vdeshpande\\Desktop\\Python_Notes\\Flask_Tutorial\\uploads'