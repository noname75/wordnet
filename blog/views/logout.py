from flask import Blueprint, redirect, flash, session, url_for

from blog import app


logout_page = Blueprint('logout', __name__, template_folder='templates')
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    flash('خروج از سایت انجام شد.', category='success')
    return redirect(url_for('index'))