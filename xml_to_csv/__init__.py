from flask import Flask, render_template, redirect
from xml_to_csv import assets
from xml_to_csv.forms import LoginForm
import os

XML2CSV=Flask(__name__)
XML2CSV.config['SECRET_KEY']=os.environ.get('SECRET_KEY') or 'vdeshpande@deloitte.com-ismyemail'

@XML2CSV.route('/')
def homepage_default():
    return redirect('/login')
    
@XML2CSV.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        return redirect('/main')
    return render_template('Login.html',form=form,title='Sign In | XML2CSV')

@XML2CSV.route('/main')
def main():
    return render_template('Main.html',title='Homepage | XML2CSV')