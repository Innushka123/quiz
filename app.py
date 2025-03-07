from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
db = SQLAlchemy(app)

# Define database models
class Participant(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), db.ForeignKey('participant.username'))
    question_id = db.Column(db.Integer)
    answer = db.Column(db.String(255))
    is_correct = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register_participant():
    """Register a new participant with username"""
    if request.method == 'POST':
        username = request.form.get('username')

        if existing_user := Participant.query.filter_by(username=username).first():
            return render_template('register.html', error="Username already taken")

        new_participant = Participant(username=username)
        db.session.add(new_participant)
        db.session.commit()

        return redirect(url_for('serve_quiz', username=username))

    return render_template('register.html')

@app.route('/quiz/<username>', methods=['GET'])
def serve_quiz(username):
    """Serve quiz to participant"""
    # Verify username exists
    participant = Participant.query.filter_by(username=username).first()
    if not participant:
        return redirect(url_for('register_participant'))

    questions_en = [
        {"question_id": 1, "text": "Babies can think logically.", "options": ["True", "False"], "answer": "True"},
        {"question_id": 2, "text": "Babies start learning language before they are born.", "options": ["True", "False"], "answer": "True"},
        {"question_id": 3, "text": "Children learn the difference between fair and unfair behavior during preschool.", "options": ["True", "False"], "answer": "True"}
    ]
    questions_de = [
        {"question_id": 1, "text": "Babys können logisch denken.", "options": ["Wahr", "Falsch"], "answer": "Wahr"},
        {"question_id": 2, "text": "Babys beginnen, Sprache zu lernen, bevor sie geboren sind.", "options": ["Wahr", "Falsch"], "answer": "Wahr"},
        {"question_id": 3, "text": "Kinder lernen den Unterschied zwischen fairem und unfairem Verhalten im Vorschulalter.", "options": ["Wahr", "Falsch"], "answer": "Wahr"}
    ]

    selected_language = request.args.get('lang', 'en')  # Default to English
    questions = questions_en if selected_language == 'en' else questions_de

    return render_template('quiz.html', username=username, questions=questions, selected_language=selected_language)

@app.route('/submit', methods=['POST'])
def submit_quiz():
    """Save quiz results"""
    data = request.json
    username = data.get('username')
    answers = data.get('answers', [])

    questions = [
        {
            "question_id": 1,
            "text": "Babies can think logically.",
            "options": ["True", "False"],
            "answer": "True"
        },
        {
            "question_id": 2,
            "text": "Babies start learning language before they are born.",
            "options": ["True", "False"],
            "answer": "True"
        },
        {
            "question_id": 3,
            "text": "Children learn the difference between fair and unfair behavior during preschool.",
            "options": ["True", "False"],
            "answer": "True"
        }
    ]

    for answer in answers:
        if question := next(
            (
                q
                for q in questions
                if q['question_id'] == answer.get('question_id')
            ),
            None,
        ):
            is_correct = answer.get('answer') == question.get('answer')
            result = QuizResult(
                username=username,
                question_id=answer.get('question_id'),
                answer=answer.get('answer'),
                is_correct=is_correct
            )
            db.session.add(result)

    db.session.commit()
    return jsonify({'success': True})

@app.route('/results')
def results_lookup():
    """Page for parents to enter username and view results"""
    return render_template('lookup.html')

@app.route('/results/lookup', methods=['POST'])
def lookup_results():
    """Look up results by username"""
    username = request.form.get('username')
    return redirect(url_for('show_results', username=username))

@app.route('/results/show/<username>')
def show_results(username):
    """Show results page for a participant"""
    # Query results for this participant
    results = QuizResult.query.filter_by(username=username).all()
    
    # Handle case where username doesn't exist
    if not results:
        return render_template('lookup.html', error="No results found for that username")
    
    # Calculate score
    total_questions = len(results)
    correct_answers = sum(1 for r in results if r.is_correct)
    score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    return render_template('results.html', 
                        username=username,
                        score=score_percentage,
                        correct=correct_answers,
                        total=total_questions)

@app.route('/admin/stats')
def admin_stats():
    """Admin page for statistics"""
    # Here you would add authentication for admin access
    
    return render_template('admin.html')

@app.route('/api/stats')
def get_stats():
    """API endpoint for statistics"""
    # Get all results
    results = QuizResult.query.all()
    
    # Convert to dataframe for analysis
    df = pd.DataFrame([{
        'username': r.username,
        'question_id': r.question_id,
        'is_correct': r.is_correct,
        'timestamp': r.timestamp
    } for r in results])
    
    # Calculate statistics
    if not df.empty:
        stats = {
            'total_participants': df['username'].nunique(),
            'average_score': (df['is_correct'].mean() * 100),
            'question_stats': df.groupby('question_id')['is_correct'].mean().to_dict(),
        }
    else:
        stats = {
            'total_participants': 0,
            'average_score': 0,
            'question_stats': {}
        }
    
    return jsonify(stats)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)