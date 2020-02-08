from flask import Flask, render_template, redirect
import jinja2

XML2CSV=Flask(__name__)

XML2CSV.config.from_object('config')
from .util import assets
from xml_to_csv import routes