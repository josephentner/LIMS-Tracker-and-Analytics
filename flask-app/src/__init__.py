from flask import Flask
from flaskext.mysql import MySQL

# create a MySQL object that will use in other parts of the API
db = MySQL()

def create_app():
    app = Flask(__name__)
    
    # secret key that will be used for securely signing the session 
    # cookie and can be used for any other security related needs
    app.config['SECRET_KEY'] = 'password1234'

    # these are for the DB object to be able to connect to MySQL. 
    app.config['MYSQL_DATABASE_USER'] = 'webapp'
    app.config['MYSQL_DATABASE_PASSWORD'] = open('/secrets/db_password.txt').readline()
    app.config['MYSQL_DATABASE_HOST'] = 'db'
    app.config['MYSQL_DATABASE_PORT'] = 3306
    app.config['MYSQL_DATABASE_DB'] = 'lims'  

    # Initialize the database object with the settings above
    db.init_app(app)
    
    # Import the various routes
    from src.analyst.analyst import analyst
    from src.assistant.assistant  import assistant
    from src.scientist.scientist import scientist

    # Register the routes that were just imported so they can be properly handled
    app.register_blueprint(analyst,       url_prefix='/analyst')
    app.register_blueprint(assistant,   url_prefix='/assistant')
    app.register_blueprint(scientist,    url_prefix='/scientist')

    return app