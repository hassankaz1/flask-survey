from http.client import responses
from flask import Flask, redirect, render_template, request, flash, session
from surveys import Question, surveys


app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

RESPONSES_KEY = "responses"


@app.route("/")
def home_page():
    """Show home page"""
    return render_template("home.html")


@app.route("/questions/<int:number>")
def show_question(number):
    # when survey starts we make session[response] = empty list
    if number == 0:
        session[RESPONSES_KEY] = []

    responses = session[RESPONSES_KEY]

    # if all questions responded then return to home page
    if(len(responses) == len(surveys["satisfaction"].questions)):
        return redirect("/finished")

    # check if the user input number themselves if they do, flash message and redirect to current question
    if(len(responses) != number):
        flash(f"Invalid question id: {number}")
        return redirect(f"/questions/{len(responses)}")

    # get current question from survey
    curr_q = surveys["satisfaction"].questions[number]
    return render_template("questions.html", q=curr_q)


@app.route("/answer", methods=["POST"])
def next_question():
    # get the response and append to our response list
    ans = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(ans)
    session[RESPONSES_KEY] = responses

    # redirect back to questions
    return redirect(f"/questions/{len(responses)}")

# completed survey page


@app.route("/finished")
def completed():
    return render_template("finished.html")
