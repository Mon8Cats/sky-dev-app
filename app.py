#
# pylint: disable=import-error
#

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World from Flask development server!"

if __name__ == "__main__":
    # Use host="0.0.0.0" to make the app externally visible
    app.run(host="0.0.0.0", port=8080)
