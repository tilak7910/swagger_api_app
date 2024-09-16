from flask_swagger_ui import get_swaggerui_blueprint

def configure_swagger(app):
    swagger_url = '/swagger'  # Swagger UI URL
    api_url = '/static/swagger.json'  # URL for Swagger JSON file
    swaggerui_blueprint = get_swaggerui_blueprint(
        swagger_url,
        api_url,
        config={
            'app_name': "Flask API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=swagger_url)
