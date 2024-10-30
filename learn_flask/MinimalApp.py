from flask import Flask
from flask import url_for
from markupsafe import escape

# ** Run the application
# To activate the .venv environment: . .venv/bin/activate
# To run this application: flask --app MinimalApp run
# Shortcut: if the file is named app.py or wsgi.py, don't have to use --app.

# ** --host option
# The server is only accessible from this computer because it is in debugging mode.
# If trust other users on your network, use option: --host=0.0.0.0
#   to tell your OS to listen on all public IPs.

# ** --debug option
# Enabling debug mode allows the server to reload automatically if code changes.
# To enable debug mode, use option: --debug
# Warning: do not run the development server or debugger in a production environment.

# ** HTML escaping
# Need to escape HTML to protect from injection attacks.
# Escaping renders things like <script>alert("bad")</script> as text, rather than running an actual script.
# Jinja will do this automatically on HTML templates.
# Use escape() from markupsafe to do this manually.

# ** Routing
# Use route() decorator to bind a function to a URL
# Can also add variable sections to a URL with <variable_name>
# Can use a converter to specify the type of the argument for <variable_name>

# ** Unique URLs vs. Redirection
# URLs like '/projects/' act like a folder.
# URLs like '/about' act like an unique URL, or the pathname of a file.

# ** URL building
# Use url_for() to build a URL to a specific function.
# The generated paths are always absolute.

# ** HTTP


app = Flask(__name__)

@app.route('/')
def index():
    return 'This is the Main Page.'

# <username> is a variable name that client can input to get to this page
# e.g.: http://127.0.0.1:5000/u will have 'Hello, u' on the page
@app.route('/<username>')
def welcome_user(username):
    return f'Hello, {username}. This is your user page'

# test_request_context() makes Flask to execute things inside this function
with app.test_request_context():
    print()
    print('URL for the index/main page:', url_for('index'))
    print()