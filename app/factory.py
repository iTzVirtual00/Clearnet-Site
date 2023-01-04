from quart import Quart, render_template

import settings

app: Quart = ...
listeners: int = 0


async def _error_handlers(app: Quart):
    @app.errorhandler(500)
    async def page_error(e):
        return await render_template('error.html', code=500, errormsg="Error occurred"), 500

    @app.errorhandler(404)
    async def page_not_found(e):
        return await render_template('error.html', code=404, errormsg="Page not found"), 404


def create_app():
    global app
    app = Quart(__name__)

    app.secret_key = settings.SECRET

    @app.before_serving
    async def startup():
        await _error_handlers(app)

        from app.routes import bp_router
        from app.api import api_router
        app.register_blueprint(bp_router)
        app.register_blueprint(api_router)

    return app
