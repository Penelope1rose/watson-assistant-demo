from flask import Flask
from flask import render_template
import os

# app = Flask(__name__)
app = Flask(__name__)

# app = Flask(static_folder='/static')

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

@app.route('/')
def index():
    return render_template('ABCBankPage.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port, debug=True)