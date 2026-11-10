from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy (app)


@app.route('/')
def home():
    return render_template('index.html')


class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    

@app.route('/question', methods=["GET", "POST"])
def questionPage():

    if request.method == 'POST':
        
        answer = request.form.get('answer', '').strip()

        if not answer:
            error = "We need a response, please give one."
            return render_template('question.html', error=error)
    

    try:
        new_answer = Answers(
            answer=answer
        )
        db.session.add(new_answer)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        error = "An error occurred while saving your response, please try again"
        return render_template('question.html', error=error)
    

    return render_template('response.html', answer=answer)


@app.route('/responses')
def answersPage():
    answers = Answers.query.all()
    return render_template('answers.html', answers=answers)



with app.app_context():
    db.create_all()
#Remember to start with python -m venv venv, and on new ones pip install flask, then use flask run --debug (Reminder for me, I forget this often)