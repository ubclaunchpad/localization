from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from .routes.server import server
    app.register_blueprint(server)
    
    return app