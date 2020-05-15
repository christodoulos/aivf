from flask import Blueprint, request, flash, redirect, url_for, render_template
from flask_login import login_required, login_user, logout_user

from lib.safe_next_url import safe_next_url

from aivf.blueprints.user.decorators import anonymous_required
from aivf.blueprints.user.forms import LoginForm
from aivf.blueprints.user.models import User

user = Blueprint('user', __name__, template_folder='templates')


@user.route('/login', methods=['GET', 'POST'])
@anonymous_required()
def login():
    form = LoginForm(next=request.args.get('next'))

    if form.validate_on_submit():

        try:
            u = User.objects.get(email=request.form.get('identity'))
        except User.DoesNotExist:
            u = None

        if u and u.authenticated(False, request.form.get('password')):
            if login_user(u, remember=True):
                #  u.update_activity_tracking(request.remote_addr)

                next_url = request.form.get('next')
                if next_url:
                    return redirect(safe_next_url(next_url))
                #  return redirect(url_for('user.settings'))
                return redirect("/")
        else:
            flash('Identity or password is incorect.', 'error')

    return render_template('user/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('user.login'))
