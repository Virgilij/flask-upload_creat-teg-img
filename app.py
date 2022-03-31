from flask import Flask, render_template, url_for, redirect, request
from flask_wtf import FlaskForm
from wtforms import FileField
from flask_uploads import configure_uploads, IMAGES, UploadSet, patch_request_class


app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisasecret'
app.config['UPLOADED_IMAGES_DEST'] = 'static/images'    # Image save path

images = UploadSet('images', IMAGES)
configure_uploads(app, images)
patch_request_class(app)    # Limits file size to 16 MB

class MyForm(FlaskForm):
    """Flask-WTF provides you with a FileField to handle file uploads, it automatically extracts
     data from flask.request.files if the form is posted. The FileField data attribute will be
     instance of Werkzeug FileStorage."""
    image = FileField('image')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()
    link = None

    if form.validate_on_submit():
        print(form.image.data)

        try:
            filename = images.save(form.image.data)     # Save the selected file to the specified folder

            link = f'<img src="/static/images/{filename}">'     # Variable to save the path to the file
            print(link)

        except:
            print("Error adding file")
            return redirect(url_for('page404'))

    return render_template('index.html', form=form, link=link)


@app.route('/show_img', methods=['GET', 'POST'])
def show_img():
    # handle the POST request
    if request.method == 'POST':
        show_link = request.form.get('show_link')

        return show_link

    return render_template('show_img.html')


@app.route('/page404')
def page404():
    return render_template('page404.html')




if __name__ == '__main__':
    app.run(debug=True)