from flask import redirect, render_template, request, url_for, Blueprint
from project.messages.models import Message
from project.users.views import ensure_correct_user
from project.messages.forms import MessageForm, LikeForm
from flask_login import current_user, login_required
from project import db
from project.users.models import User

messages_blueprint = Blueprint(
    'messages', __name__, template_folder='templates')


@messages_blueprint.route('/', methods=["POST"])
@login_required
def index(id):
    if current_user.get_id() == str(id):
        form = MessageForm()
        if form.validate():
            new_message = Message(text=form.text.data, user_id=id)
            db.session.add(new_message)
            db.session.commit()
            return redirect(url_for('users.show', id=id))
    return render_template('messages/new.html', form=form)


@messages_blueprint.route('/new')
@login_required
@ensure_correct_user
def new(id):
    return render_template('messages/new.html', form=MessageForm())


@messages_blueprint.route(
    '/<int:message_id>/likes', methods=['POST', 'DELETE'])
@login_required
@ensure_correct_user
def like_add_del(id, message_id):
    user = User.query.get_or_404(id)
    form = LikeForm(request.form)

    if request.method == 'POST':
        if form.validate():
            user.message_likes.append(Message.query.get_or_404(message_id))
            db.session.commit()
            return redirect(url_for('users.likes', id=id))
        return redirect(url_for('users.index'))
    if request.method == b'DELETE':

        if form.validate():
            user.message_likes.remove(Message.query.get_or_404(message_id))
            db.session.commit()
            return redirect(url_for('users.likes', id=id))
        return redirect(url_for('users.index'))
    return "you forgot b "


@messages_blueprint.route('/<int:message_id>', methods=["GET", "DELETE"])
def show(id, message_id):
    found_message = Message.query.get_or_404(message_id)
    form = LikeForm()
    if request.method == b"DELETE" and current_user.id == id:
        db.session.delete(found_message)
        db.session.commit()
        return redirect(url_for('users.show', id=id))
    return render_template(
        'messages/show.html', id=id, message=found_message, form=form)
