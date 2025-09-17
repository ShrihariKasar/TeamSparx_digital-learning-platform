# Configurations (DB, secrets, etc.) 
import os

class Config:
    # Flask secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey123'

    # MySQL Database configuration
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = 'root2'
    DB_NAME = 'd_learning_platform'

    # SQLAlchemy Database URI
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload folder for content (pdf/video/images)
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')

    # Optional: allowed file types
    ALLOWED_EXTENSIONS = {'pdf', 'mp4', 'png', 'jpg', 'jpeg'}