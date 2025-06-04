
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'CRM для компьютерного клуба — работает!'

if __name__ == '__main__':
    app.run(debug=True)
