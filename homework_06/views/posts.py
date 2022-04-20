from http import HTTPStatus

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
)
from sqlalchemy.exc import IntegrityError, DatabaseError
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError

from forms import PostForm
from models import Post, User
from models.database import db

posts_app = Blueprint("posts_app", __name__)


def create_posts(posts_data: list[dict]):
    result: list[User] = User.query.all()

    users = {user.username: user.id for user in result}

    print(users)

    for p in posts_data:
        if p['username'] in users:
            post = Post(
                id=p['id'],
                title=p['title'],
                body=p['body'],
                user_id=users[p['username']],
            )
            db.session.add(post)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise BadRequest(f"could not save posts")
    except DatabaseError:
        db.session.rollback()
        raise InternalServerError(f"could not save posts, unexpected error")


@posts_app.get("/", endpoint="posts_list")
def list_posts():
    posts: list[Post] = Post.query.all()
    return render_template("posts/list.html", posts=posts)


@posts_app.get("/<int:post_id>/", endpoint="post_details")
def get_post(post_id: int):
    post = Post.query.get(post_id)
    if post is None:
        raise NotFound(f"Post #{post_id} not found!")

    return render_template(
        "posts/details.html",
        post=post,
    )


@posts_app.get("/user/<int:user_id>/", endpoint="user_post_list")
def get_user_post_list(user_id: int):
    posts: list[Post] = Post.query.filter_by(user_id=user_id)

    return render_template("posts/list.html", posts=posts, user_id=user_id)


@posts_app.route("/add/", methods=["GET", "POST"], endpoint="add")
def add_post():
    form = PostForm()
    if request.method == "GET":
        return render_template("posts/add.html", form=form)

    if not form.validate_on_submit():
        return render_template("posts/add.html", form=form), HTTPStatus.BAD_REQUEST

    title = form.data["title"]
    body = form.data["body"]
    user_id = form.data["user_id"]
    post = Post(title=title, body=body, user_id=user_id)
    db.session.add(post)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise BadRequest(f"could not save post")
    except DatabaseError:
        db.session.rollback()
        raise InternalServerError(f"could not save post, unexpected error")

    post_url = url_for("posts_app.post_details", post_id=post.id)
    return redirect(post_url)
