import settings
from app.factory import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host=settings.HOST, port=settings.PORT, use_reloader=False)
