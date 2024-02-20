# I still haven't implemented Step 8 (session) - will come back to it!

from flask import Flask, request, render_template, redirect, flash
from surveys import *
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def show_homepage():
    """Show homepage and redirect to the question page."""
    return render_template('home.html', title=satisfaction_survey.title, instructions=satisfaction_survey.instructions)

@app.route('/begin')
def start_survey():
    """Clear the responses when user starts the survey."""

    responses = []
    return redirect('/question/0')

@app.route('/question/<int:question_num>')
def question_page(question_num):
    """Ask question and show choices."""

    if responses is None:
        # Redirect user if they try to access question URL too soon
        return redirect('/')

    if len(responses) == len(satisfaction_survey.questions):
        # Redirect user to end page if the survey is complete
        return redirect('/complete')

    if question_num != len(responses):
        # Redirect user to correct question if they try to skip a question
        flash("You're trying to access an invalid question!")
        return redirect(f'/question/{len(responses)}')
    
    # Retrieve question from satisfaction survey
    question_instance = satisfaction_survey.questions[question_num]

    return render_template('question.html', question=question_instance.question, choices=question_instance.choices)

@app.route('/answer', methods=["POST"])
def answer_page():
    
    choice = request.form['choices']
    responses.append(choice)
    print(responses)
    # Check if user has answered the last question
    if len(responses) == 4:
        return redirect('/complete')

    return redirect(f"/question/{len(responses)}")

@app.route('/complete')
def completed():
    return "Thank you for taking the survey!"
