from http.client import responses
from flask import Flask, redirect, render_template, request, flash
from surveys import Question, surveys


app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

responses = []


@app.route("/")
def home_page():
    """Show home page"""
    return render_template("home.html")


@app.route("/questions/<number>")
def show_question(number):
    # if all questions responded then return to home page
    if(len(responses) == len(surveys["satisfaction"].questions)):
        return redirect("/finished")

    # turn number to int from string
    num = int(number)

    # check if the user input number themselves if they do, flash message and redirect to current question
    if(len(responses) != num):
        flash(f"Invalid question id: {num}")
        return redirect(f"/questions/{len(responses)}")

    # get current question from survey
    curr_q = surveys["satisfaction"].questions[num]
    return render_template("questions.html", q=curr_q)


@app.route("/answer", methods=["POST"])
def next_question():
    # get the response and append to our response list
    ans = request.form['answer']
    responses.append(ans)
    # redirect back to questions
    return redirect(f"/questions/{len(responses)}")

# completed survey page


@app.route("/finished")
def completed():
    return render_template("finished.html")
