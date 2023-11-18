from application import app
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    PORT = os.environ.get('PORT_DEV')
    DEBUG = os.environ.get('FLASK_DEBUG')
    HOST = os.environ.get('HOST_DEV')
    app.run(host=HOST, port=PORT, debug=DEBUG)

app.config['RECAPTCHA_PUBLIC_KEY'] = 'your_recaptcha_public_key'
app.config['RECAPTCHA_PRIVATE_KEY'] = 'your_recaptcha_private_key'
    

if __name__ == "__main__":
    main()