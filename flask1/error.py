from flask import render_template,Blueprint


error = Blueprint('error',__name__)

@error.errorhandler(403)
def unauthorised():
    return render_template('unauthorised.html'),403

