from os import getenv

from flask import Flask
from flask_migrate import Migrate

from models.database import db
from views.users import users_app, create_users
from views.posts import posts_app, create_posts

from jsonplaceholder_requests import get_data
import asyncio

app = Flask(__name__)

CONFIG_OBJECT_PATH = "config.{}".format(getenv("CONFIG_NAME", "DevelopmentConfig"))
app.config.from_object(CONFIG_OBJECT_PATH)
db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(users_app, url_prefix="/users")
app.register_blueprint(posts_app, url_prefix="/posts")

SQLA_ECHO = True


async def async_main():
    users_data: list[dict]
    posts_data: list[dict]
    users_data, posts_data = await get_data()

    for p in posts_data:
        for u in users_data:
            if p['userId'] == u['id']:
                p['username'] = u['username']
                break

    create_users(users_data)
    create_posts(posts_data)


# @app.route("/")
@app.get("/")
def hello_world():
    return "<p>Hello, World!!!</p><br/>" \
           "<a href='/init'>init</a><br/>" \
           "<a href='/users'>users</a><br/>" \
           "<a href='/posts'>posts</a>"


@app.get("/init")
def init_db():
    asyncio.run(async_main())
    return "<p>Done!!!</p>"


if __name__ == '__main__':
    app.run(host="0.0.0.0")
