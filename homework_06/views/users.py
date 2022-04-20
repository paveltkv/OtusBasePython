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

from forms import UserForm
from models import User
from models.database import db

users_app = Blueprint("users_app", __name__)


def create_users(users_data: list[dict]):
    for user in users_data:
        user = User(
            name=user['name'],
            username=user['username'],
            email=user['email']
        )
        db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise BadRequest(f"could not save users")
    except DatabaseError:
        db.session.rollback()
        raise InternalServerError(f"could not save users, unexpected error")


@users_app.get("/", endpoint="users_list")
def list_users():
    users: list[User] = User.query.all()
    return render_template("users/list.html", users=users)


@users_app.get("/<int:user_id>/", endpoint="user_details")
def get_user(user_id: int):
    user = User.query.get(user_id)
    if user is None:
        raise NotFound(f"User #{user_id} not found!")

    return render_template(
        "users/details.html",
        user=user,
    )


@users_app.route("/add/", methods=["GET", "POST"], endpoint="add")
def add_user():
    form = UserForm()
    if request.method == "GET":
        return render_template("users/add.html", form=form)

    if not form.validate_on_submit():
        return render_template("users/add.html", form=form), HTTPStatus.BAD_REQUEST

    user_name = form.data["name"]
    username = form.data["username"]
    email = form.data["email"]
    user = User(name=user_name, username=username, email=email)
    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise BadRequest(f"could not save user, probably name {user_name!r} is not unique")
    except DatabaseError:
        db.session.rollback()
        raise InternalServerError(f"could not save user, unexpected error")

    user_url = url_for("users_app.user_details", user_id=user.id)
    return redirect(user_url)


@users_app.get("/delete/<int:user_id>/", endpoint="delete")
def delete_user(user_id: int):
    user = User.query.get(user_id)
    if user is None:
        raise NotFound(f"User #{user_id} not found!")

    print(user)
    print(user_id)
    db.session.delete(user)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise BadRequest(f"could not delete user")
    except DatabaseError:
        db.session.rollback()
        raise InternalServerError(f"could not delete user, unexpected error")

    user_url = url_for("users_app.users_list")
    return redirect(user_url)

"""
User.query.filter(User.id == user_id).delete()

"""





