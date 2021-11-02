from flask_login import login_required, current_user
import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, send_file, Blueprint, flash
from werkzeug.utils import secure_filename
import tools

views = Blueprint('views', __name__)

ALLOWED_EXTENSIONS = {"txt","jpeg","pdf","png","jpg"}
UPLOAD_FOLDER = './uploads/'
app = Flask(__name__)
app.secret_key = os.urandom(30)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/')
def call_page_upload():
	return render_template('dashboard.html')

@views.route("/dashboard", methods=["post","get"])
@login_required
def dashboard():
	error = None
	filename = None
	if request.method == "POST":
		if "file" not in request.files:
			error = "File not selected"
			return render_template("dashboard.html", error=error)
		file = request.files["file"]
		filename = file.filename

		if filename == "":
			error = "No file chosen"
			return render_template("dashboard.html",user=current_user, error=error)
		if allowed_file(filename) == False:
			error = "File is not allowed"
			return render_template("dashboard.html",user=current_user, error=error)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
	
	return render_template("dashboard.html", user=current_user, filename=filename)




