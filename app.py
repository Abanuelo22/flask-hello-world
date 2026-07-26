from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World from Alex Banuelos in 3308"


if __name__ == "__main__":
    app.run(debug=True)
