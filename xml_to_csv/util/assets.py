from flask_assets import Bundle, Environment
from .. import XML2CSV

bundles = {
    'javascript_source':Bundle(
        'js/Myscript2.js',
        output='gen/Myscript2.js'),
    'javascript_result':Bundle(
        'js/Result_XML_Checkboxes.js',
        output='gen/Result_XML_Checkboxes.js'),
    'css_source':Bundle(
        'css/Mystyle.css',
        output='gen/Mystyle.css')
}

assets=Environment(XML2CSV)
assets.register(bundles)
