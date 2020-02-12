from flask_assets import Bundle, Environment
from .. import XML2CSV

bundles = {
    'javascript_source':Bundle(
        'js/base.js',
        output='gen/base.js'),
    'javascript_result':Bundle(
        'js/Result_XML_Checkboxes.js',
        output='gen/Result_XML_Checkboxes.js'),
    'css_source':Bundle(
        'css/base.css',
        output='gen/base.css')
}

assets=Environment(XML2CSV)
assets.register(bundles)
