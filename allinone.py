from flask import Flask 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'

from app import app 
from flask import render_template

from flask_wtf import FlaskForm #wt forms
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 

class AddTaskForm(FlaskForm):
    hashtag = StringField('hashtag', validators=[DataRequired()])
    noft = StringField('noft', validators=[DataRequired()])
    lng = StringField('lng', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/',methods=['GET','POST'])
@app.route('/index.html', methods=['GET','POST'])
def index():
    form = forms.AddTaskForm()
    print("Submitted title 1 ",form.hashtag.data)
    if form.validate_on_submit():
        return render_template('index.html',form=form,hashtag=form.hashtag.data)
    return render_template('index.html',form=form)


if __name__ == '__main__':
    app.run(debug=True)
