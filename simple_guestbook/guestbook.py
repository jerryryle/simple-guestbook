from flask import escape, Flask, g, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix
from .guestbook_file import GuestbookFile
import datetime

"""This determines the environment variable prefix that this application will use for configuration.
    Mandatory environment variables needed to configure this application:
        FILENAME - The full path to the file that will hold guestbook entries.
        
    If, for example, the prefix is set to 'GUESTBOOK' then the full FILENAME environment variable would be:
        GUESTBOOK_FILENAME 
"""
config_prefix = 'GUESTBOOK'

# Create the Flask Application and configure it
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_prefixed_env(prefix=config_prefix)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)


def get_guestbook_file():
    """Returns the guestbook file from the application context, creating one if needed."""
    if not hasattr(g, 'guestbook_file'):
        guestbook_filename = app.config.get("FILENAME", None)
        if guestbook_filename is None:
            raise Exception(f"{config_prefix}_FILENAME is not set. This environment variable is mandatory.")

        g.guestbook_file = GuestbookFile()
        g.guestbook_file.open(guestbook_filename)
    return g.guestbook_file


@app.teardown_appcontext
def teardown_guestbook_file(exception):
    """Closes the guestbook file when the application shuts down."""
    gbf = g.pop('guestbook_file', None)
    if gbf is not None:
        gbf.close()


@app.route("/")
def root():
    """This handles the root ('/') URL and serves the guestbook form"""
    return render_template('index.html')


@app.route("/guestbook.css")
def guestbook_css():
    """This handles the guestoobk.css URL and serves the guestbook CSS file"""
    return render_template('guestbook.css')

@app.route("/guestbook_post", methods=['POST'])
def guestbook_post():
    """The guestbook form posts to this URL. If the form parameters are valid, it saves them to the guestbook and
    returns the 'thank you' page. Otherwise, it returns the guestbook form along with an error flag so that the
    guestbook form can inform the user that they didn't correctly fill out the form. It also passes along what the
    user did enter so that they don't need to enter it again."""
    guest_name = ""
    guest_email = ""
    guest_message = ""
    error = False

    if request.method == 'POST':
        # Get the values for all the form fields.
        guest_name = request.form.get('guest_name', default='')
        guest_email = request.form.get('guest_email', default='')
        guest_message = request.form.get('guest_message', default='')

        if guest_message:
            # If the user supplied a non-empty message, save the submission.
            with get_guestbook_file() as gbf:
                gbf.write("--------------------------------------------------------------------------------\n")
                gbf.write(f"[{datetime.datetime.now().strftime('%B %d, %Y @ %I:%M:%S %p')}]\n")
                gbf.write(f"Guest Name: {guest_name}\n")
                gbf.write(f"Guest Email: {guest_email}\n")
                gbf.write("Guest Message:\n")
                gbf.write(f"{guest_message}\n\n")

            # Return the thank-you page, showing the user what they submitted.
            return render_template(
                'thankyou.html',
                guest_name=guest_name,
                guest_email=guest_email,
                guest_message=guest_message)
        else:
            # If the user left the message empty, return the guestbook form again with the error set to true.
            error = True

    # Default to returning the guestbook form again with any error noted and input from the user preserved.
    return render_template(
        'index.html',
        guest_name=guest_name,
        guest_email=guest_email,
        guest_message=guest_message,
        error=error)
