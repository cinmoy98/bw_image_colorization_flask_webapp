from flask import Flask, render_template, flash, request, redirect, session
import os
from werkzeug.utils import secure_filename
import shutil
import bw2color
import numpy as np
import cv2 as cv

app = Flask(__name__)

shutil.rmtree('./static/images')
os.mkdir('./static/images')

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		print("post success")
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			UPLOAD_FOLDER = './static/images/'
			file.save(os.path.join(UPLOAD_FOLDER, filename))
			print(filename)
			global imagename
			imagename = filename

			# data = pd.read_csv("./static/"+str(filename))

	return render_template('index.html')

@app.route('/showheader', methods=['GET', 'POST'])
def show_dataframe():
	if request.method == 'POST':
		showed = True
		path = bw2color.colorify(imagename)
		return render_template('home.html', path = path)

def delete_file():
	shutil.rmtree('./static/images')

if __name__=='__main__':
	app.secret_key = 'super secret key'
	app.run(debug=True)