from flask import Flask, render_template, request, flash
import chatgpt

app = Flask(__name__)


@app.route("/home", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        name = request.form.get("name_input")
        rating = request.form.get("rating_input")
        cost = request.form.get("cost_input")
        reason = request.form.get("reason_input")

        message = "There is a software program I am considering to buy. "
        message += f"Its called {name}."
        message += f" It has the rating {rating} out of 5."
        message += f" It costs me {cost}."
        message += f" I would like to use it because {reason}."
        message += " Should I buy it? Could you please summarize it in few sentences"

        reply = chatgpt.query(message)

        return render_template("index.html", reply=reply)
