# XML/XSD Parser
This Flask app with an easy-to-use frontend is intended for generating a configuration excel, given an input XML/XSD file (Extensible Markup format to Relational schema)

**_This module was used as a proof-of-concept for an internal use-case._**


## Overview

1. After logging in, one must upload an XML/XSD File, select a file-format, a destination data delimiter (default: comma), and a filename for the final config file (default: original filename with timestamp).
2. The hierarchy of parsed XML/XSD selectable tags is displayed and one needs to choose a section of these tag(s), and define the Primary key tag, Primary child tag, and Primary parent tag.
3. Finally, the config excel file for the parsed XML/XSD Tags is created at server side, so that the Spark-Scala code can access and read the XML files from Unix directory.

![process_flow](https://github.com/vikrantdeshpande09876/XML_to_CSV_Rep/tree/master/Application%20Metadata/Process_flow_flask_app.jpg?raw=True)



![process_flow](/Application%20Metadata/Process_flow_flask_app.jpg?raw=True)



## Step-by-step guide to setup the XML/XSD Parser

1.	Install GIT (This repository used 2.25.1 on Windows10): [Git](https://git-scm.com/downloads)

2.	Install Python (This application was built on 3.8.1): [Python](https://www.python.org/downloads/)

3.	Download this repository: [XML/XSD to CSV](https://github.com/vikrantdeshpande09876/XML_to_CSV_Rep)

4.	Create a virtual environment for making a copy of your system-wide Python interpreter, in the directory for this repo:
```
> python -m venv myvirtualenv
```

5.	Activate this virtual environment. You need not perform step#4 each time for execution:
```
> myvirtualenv\Scripts\activate
```

6.	Install the application-specific dependencies by executing:
```
> pip install -r requirements.txt
```

7.	Set the starting point for running this Flask application as run.py:
```
> set flask_app=run.py
```

8.	Execute the application:
```
> flask run
```

9.	In a web-browser, navigate to the URL mentioned in the cmd output from above command. For example http://127.0.0.1:5000/ or http://localhost:5000/

10.	Currently the application accepts (username, password) from the excel file Login_creds.xlsx for logging in. This file is located in the /static/ folder of the application.