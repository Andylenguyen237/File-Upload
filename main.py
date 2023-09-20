from flask import Flask, render_template, request, redirect, url_for, abort
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os 

app = Flask(__name__)
# create secret key in order for the form to show up in the template
app.config['SECRET_KEY'] = 'mykey'
app.config["UPLOAD_EXTENSIONS"] = ['.png']
app.config['UPLOAD_FOLDER'] = 'static/files'


class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")

@app.route("/", methods = ["GET", "POST"]) # send request to the server and get from the server
@app.route('/home', methods = ["GET", "POST"])
def index():

    form = UploadFileForm()

    if request.method == "POST":
        uploadfile = request.files['file']
        if uploadfile.filename != '' and allowed_extensions(uploadfile.filename) == True:
            filename = secure_filename(uploadfile.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            uploadfile.save(filepath)
            return "File has been uploaded"
        return redirect(url_for('index'))
    return render_template('index.html', form = form)

def allowed_extensions(filename):
    file_ext = os.path.splitext(filename)[1]
    print(file_ext)
    if file_ext not in app.config["UPLOAD_EXTENSIONS"]:
        abort(400)
    return True

    # -- 
    #if form.validate_on_submit():
         # grab the file
    #    file = form.file.data
        # save file 
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        #myfile.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(myfile.filename)))
        # display message
    #    return "File has been uploaded"
    #return render_template('index.html', form=form)


#def upload_files():
#    upload_file = request.files['file']
#    filename = secure_filename(upload_file.filename)
#    if filename != '':
#        # check coorect extension 
#        file_ext = os.path.splitext(filename)[1]
#        if file_ext not in app.config['UPLOAD_EXTENSIONS']: abort(400)
#        # save 
#        upload_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
#    return redirect(url_for('index'))
    

if __name__ == '__main__':
    app.run(debug=True)