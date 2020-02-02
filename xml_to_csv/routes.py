from flask import Flask, render_template, redirect, request, flash, session
from xml_to_csv.forms import LoginForm
from . import XML2CSV
from xml_to_csv.main import Main
import os

@XML2CSV.route('/')
def homepage_default():
    return redirect('/login')
    
@XML2CSV.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        if str.lower(form.username.data)=='vikrant' and form.password.data=='vdeshpande@123':
            return redirect('/home')
        else:
            flash('Incorrect username or password. Please try again.')
            return redirect('/login')
    return render_template('Login.html',form=form,title='Sign In | XML2CSV')

@XML2CSV.route('/home',methods=['GET','POST'])
def home():
    if request.method=='POST' and request.files:
        if str.lower('.'+request.form['ftype']) in request.files['filename'].filename:
            selected_file=request.files['filename']
            filename=selected_file.filename
            selected_ftype=request.form['ftype']
            path=os.path.join(XML2CSV.config['UPLOAD_DIR'],filename)
            try:
                selected_file.save(path)
                session['path']=path
                session['selected_ftype']=selected_ftype
                session['filename']=filename
                flash(selected_ftype+" file "+filename+" saved successfully! Uploaded at: "+str(path))
            except Exception as e:
                flash("File couldn't be saved! :( \n"+e)
            return redirect('/result')
        else:
            flash('Please ensure you upload the correct file format!')
            return redirect('/login')
    return render_template('Home.html',title='Home | XML2CSV')

@XML2CSV.route('/result')
def result():
    if session['filename'] and session['selected_ftype']:
        main=Main()
        path=session['path']
        filename=session['filename']
        selected_ftype=session['selected_ftype']
        main.exec_main_functions(path, selected_ftype)
        df_x=main.retrieve_dataframe(main.x)
        main.write_dataframe_to_csv(XML2CSV.config['UPLOAD_DIR'],filename,df_x,',')
    else:
        print("Could not find session variables!")
    return render_template('Result.html',title="Result | XML2CSV")