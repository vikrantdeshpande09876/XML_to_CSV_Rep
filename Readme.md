# XML/XSD Parser
This Flask app with an easy-to-use frontend is intended for generating a configuration excel, given an input XML/XSD file (Extensible Markup format to Relational schema).

**_This module was used as a proof-of-concept for an internal use-case._**


## Overview

<ol>
<li>This Flask Application is live on <a href="https://xmlxsdparser.herokuapp.com/" target="blank">Heroku</a> for demonstration purposes.</li>
<li>After logging in, one must upload an XML/XSD File, select a file-format, a destination data delimiter (default: comma), and a filename for the final config file (default: original filename with timestamp).</li>
<li>The hierarchy of parsed XML/XSD selectable tags is displayed and one needs to choose a section of these tag(s), and define the Primary key tag, Primary child tag, and Primary parent tag.</li>
<li>
The config file will mainly contain a hierarchy of nested-tags of your XML/XSD file (with associated metadata for the downstream Pyspark application) as:
<ul>
<li>Parent1</li>
<li>Parent1.child1</li>
<li>Parent1.child2</li>
<li>Parent1.child2.subchild1</li>
<li>Parent1.child2.subchild2</li>
</ul>
</li>
<li>Finally, the config excel file for the parsed XML/XSD Tags is created at server side, so that the Spark-Scala code can access and read the XML files from Unix directory.</li>
</ol>

![process_flow](/Application%20Metadata/Process_flow_flask_app.jpg?raw=True)



## Step-by-step guide to setup the XML/XSD Parser

1.	Install GIT (This repository used 2.25.1 on Windows10): [Git](https://git-scm.com/downloads)

2.	Install Python (This application was built on 3.8.1): [Python](https://www.python.org/downloads/)

3.	Clone the current repository: [XML/XSD to CSV](https://github.com/vikrantdeshpande09876/XML_to_CSV_Rep)

4.	Navigate to the directory for this repo, and create a virtual environment for making a copy of your system-wide Python interpreter:
```
> python -m venv myvirtualenv
```

5.	Activate this virtual environment. You need not perform step#4 each time for execution:
```
> myvirtualenv\Scripts\activate
```

6.	Install the application by executing:
```
> pip install -e .
```

7.	Set the starting point for running this Flask application as the package where our application 'xml_to_csv' lives:
```
> set flask_app=xml_to_csv
> set flask_env=development
```

8.	Execute the application from any directory on your system:
```
> flask run
```

9.	In a web-browser, navigate to the URL mentioned in the cmd output from above command. For example http://127.0.0.1:5000/ or http://localhost:5000/. App is currently live on [Heroku](https://xmlxsdparser.herokuapp.com/) to view.

10.	Currently the application accepts (username, password) from the excel file Login_creds.xlsx for logging in. This file is located in the /xml_to_csv/static/ folder of the application. These static login-credentials were used for quick development of a Minimal Viable Product.