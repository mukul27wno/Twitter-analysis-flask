from app import app 
from flask import render_template

import forms

@app.route('/',methods=['GET','POST'])
@app.route('/index.html', methods=['GET','POST'])
def index():
    form = forms.AddTaskForm()
    print("Submitted title 1 ",form.hashtag.data)
    if form.validate_on_submit():
        print("Submitted title",form.hashtag.data)
        return render_template('result.html',form=form,hashtag=form.hashtag.data)
    return render_template('index.html',form=form)
