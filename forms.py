from flask_wtf import FlaskForm #wt forms
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 

class AddTaskForm(FlaskForm):
    hashtag = StringField('hashtag', validators=[DataRequired()])
    noft = StringField('noft', validators=[DataRequired()])
    lng = StringField('lng', validators=[DataRequired()])
    submit = SubmitField('Submit')