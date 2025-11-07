from flask import render_template, session, redirect, url_for, current_app, flash
from .. import db
from ..models import User
from ..email import send_email, send_simple_message
from . import main
from .forms import NameForm

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        username = form.name.data
        user = User.query.filter_by(username=username).first()
        if user is None:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
            session['known'] = False

            admin = current_app.config.get('FLASKY_ADMIN')
            if admin:
                try:
                    send_simple_message([admin],
                                        'Novo usuário',
                                        f'Novo usuário: {username} - email: {form.email.data or "não informado"}')
                    flash('E-mail enviado para o Administrador do sistema, notificando o cadastro de um novo usuário.', 'success')
                except Exception as e:
                    flash('Falha ao enviar o e-mail de notificação: ' + str(e), 'danger')
        else:
            session['known'] = True

        session['name'] = username
        return redirect(url_for('.index'))

    users = User.query.order_by(User.username).all()
    return render_template('index.html',
                           form=form,
                           name=session.get('name'),
                           known=session.get('known', False),
                           users=users)
