from flask import Flask, render_template, request

# Configure app
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/greet", methods=["POST"])
def greet():
    name = request.form.get("name")
    greet = f"Hello, {name}!"
    return greet

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port="5000")