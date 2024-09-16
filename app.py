from flask import Flask
from config import Config
from routes import bp as routes_bp
from swagger import configure_swagger
from otel_config import configure_opentelemetry
from extensions import db, jwt, migrate
from flask_cors import CORS
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    # Configure Swagger and OpenTelemetry
    configure_swagger(app)
    configure_opentelemetry(app)
    
    # Register Blueprints
    app.register_blueprint(routes_bp)

    return app

def test_database_connection(app):
    try:
        # Extract database configuration
        config = app.config
        user = config['MYSQL_USER']
        password = config['MYSQL_PASSWORD']
        host = config['MYSQL_HOST']
        database = config['MYSQL_DB']
        port = config.get('MYSQL_PORT', 3306)

        # Create the connection string
        connection_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
        engine = create_engine(connection_string)
        
        # Attempt to connect
        with engine.connect() as connection:
            print("Database connection successful!")
    except OperationalError as e:
        print("Database connection failed:", e)

if __name__ == "__main__":
    app = create_app()
    
    # Validate the database connection
    test_database_connection(app)
    
    # Run the application
    app.run(debug=True, port=5001)
