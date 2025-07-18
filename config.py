import os
from   decouple import config

class Config(object):

    VERSION = "v0.0.3"
    
    basedir    = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')

    # This will create a file in $HOME/.Nextpie folder
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join("~", ".Nextpie", 'nextpie-DB.sqlite3')
    
    # This will create a file in app folder
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    ## Upload
    UPLOAD_FOLDER = os.path.join(basedir,"uploads")
    UPLOAD_EXTENSIONS = ['txt']
    MAX_CONTENT_LENGTH = 1024 * 1024 * 5
    
    ENV = "development"
    
    FLASK_ADMIN_FLUID_LAYOUT = True


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY  = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config( 'DB_ENGINE'   , default='postgresql'),
        config( 'DB_USERNAME' , default='user'),
        config( 'DB_PASS'     , default='pass'),
        config( 'DB_HOST'     , default='localhost'),
        config( 'DB_PORT'     , default=5000),
        config( 'DB_NAME'     , default='nextpie' )
    )

class DebugConfig(Config):
    DEBUG = True

# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
