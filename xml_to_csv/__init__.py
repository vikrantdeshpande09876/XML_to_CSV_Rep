from warnings import simplefilter
from flask import Flask, render_template, redirect
from flask_assets import Bundle, Environment

# Factory method to create the Flask-app instance
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    if test_config is None:
        app.config.from_object('config')
    else:
        app.config.from_object(test_config,silent=True)
    
    @app.route('/hello')
    def hello():
        return "hello world. Starting-page for test."
    
    from . import routes

    bundles = {
        'javascript_source':Bundle(
            'js/base.js', output='gen/base.js'),
        'javascript_result':Bundle(
            'js/Result_XML_Checkboxes.js', output='gen/Result_XML_Checkboxes.js'),
        'css_source':Bundle(
            'css/base.css', output='gen/base.css')
    }

    assets = Environment(app)
    assets.register(bundles)
    app.register_blueprint(routes.bp)
    return app