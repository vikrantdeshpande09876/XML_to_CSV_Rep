import os
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY') or 'vikrant.deshpande09876@gmail.com-ismyemail'
UPLOAD_DIR = os.environ.get('UPLOAD_DIR') or os.path.join(os.path.dirname(__file__), 'uploads')
STATIC_DIR = os.environ.get('STATIC_DIR') or os.path.join(os.path.dirname(__file__), 'xml_to_csv', 'static')