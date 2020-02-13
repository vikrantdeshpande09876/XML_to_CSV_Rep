from flask import Flask, render_template, redirect, request, flash, session, render_template_string
from .forms import LoginForm
from . import XML2CSV
from .main import Main
import os
import json
from re import sub

@XML2CSV.route('/')
def homepage_default():
    return redirect('/login')
    
@XML2CSV.route('/login',methods=['GET','POST'])
def login():
    if 'validated' in session:
        return redirect('/home')
    form=LoginForm()
    if form.validate_on_submit():
        if str.lower(form.username.data)=='v' and form.password.data=='v':
            session['validated']=True
            return redirect('/home')
        else:
            flash('Incorrect username or password. Please try again.')
            return redirect('/login')
    return render_template('Login.html',form=form,title='Sign In | XML2CSV')

@XML2CSV.route('/home',methods=['GET','POST'])
def home():
    if 'validated' in session:
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
                    flash("File couldn't be saved! \n"+e)
                return redirect('/home/displayTags')
            else:
                flash('Please ensure you upload the correct file format!')
                return redirect('/login')
        return render_template('Home.html',title='Home | XML2CSV')
    else:
        flash('You must be signed in to view that page!')
        return redirect('/login')

@XML2CSV.route('/result')
def result():
    if 'validated' in session:
        print("Hello Vikrant Deshpande")
    else:
        flash('You must be signed in to view that page!')
        return redirect('/login')
    return render_template('Result.html', title="Result | XML2CSV")











@XML2CSV.route('/home/displayTags',methods=['GET','POST'])
def displayTags():
    if 'validated' in session:
        if 'filename' in session and 'selected_ftype' in session and 'path' in session:
            main=Main()
            overallstring=main.exec_main_functions(session['path'], session['selected_ftype'])
            overallstring='{%extends "base.html"%}{%block content%}'+'{%assets "javascript_result"%}<script src="{{ ASSET_URL }}"></script>{%endassets%}<div id="root" class="container"><h1>'+session['filename']+' Tags | XML2CSV</h2>'+overallstring+'</div>{%endblock%}'
        else:
            flash("Could not find session variables! Please try to refresh the page.")
    else:
        flash('You must be signed in to view that page!')
        return redirect('/login')
    return render_template_string(overallstring, title="Result | XML2CSV")



@XML2CSV.route('/home/result',methods=['GET','POST'])
def home_result():
    if 'validated' in session:
        if 'filename' in session and 'selected_ftype' in session and 'path' in session:
            for key in request.form.keys():
                    data=key
            #print("The raw data is= "+str(data))    #retrieves a JSON object with 0th element as our passed object from JS
            res_array=json.loads(data)['res_array']
            try:
                main=Main()
                df=main.retrieve_dataframe(res_array)
                main.write_dataframe_to_csv(sub(session['filename'],'',session['path']),session['filename'],df,'|')
                print("Your dataframe was written successfully into the config.csv File!")
            except Exception as e:
                print("Could not process into the config.csv File! Error is: "+str(e))
        else:
            print("Could not find the session variables. Please retry.")
            return redirect('/login')
    else:
        flash('You must be signed in to view that page!')
        return redirect('/login')
    return render_template('Result.html', title="Result | XML2CSV")
