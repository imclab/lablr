from app import app


def index():
    return app.send_static_file('html/index.html')
