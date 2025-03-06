# quiz

# Quiz Application

This is a simple quiz application built with Flask and SQLAlchemy. The application allows users to register, take quizzes, and view their results. It also includes an admin page for viewing statistics.

## Features

- User registration
- Quiz participation
- Viewing quiz results
- Admin statistics page
- API endpoint for statistics

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Innushka123/quiz.git
    cd quiz
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Run the application:
    ```sh
    python app.py
    ```

## Project Structure

- [app.py](http://_vscodecontentref_/1): Main application file containing routes and database models.
- [templates](http://_vscodecontentref_/2): Directory containing HTML templates for rendering pages.
- [quiz.db](http://_vscodecontentref_/3): SQLite database file.

## Routes

- `/`: Home page.
- `/register`: Register a new participant.
- `/quiz/<username>`: Serve quiz to a participant.
- `/submit`: Save quiz results (POST).
- `/results`: Page for parents to enter username and view results.
- `/results/lookup`: Look up results by username (POST).
- `/results/show/<username>`: Show results page for a participant.
- `/admin/stats`: Admin page for statistics.
- `/api/stats`: API endpoint for statistics.

## Database Models

- [Participant](http://_vscodecontentref_/4): Model representing a quiz participant.
    - [username](http://_vscodecontentref_/5): Primary key, string.
    - [created_at](http://_vscodecontentref_/6): DateTime, default is the current time.

- [QuizResult](http://_vscodecontentref_/7): Model representing a quiz result.
    - [id](http://_vscodecontentref_/8): Primary key, integer.
    - [username](http://_vscodecontentref_/9): Foreign key to [Participant.username](http://_vscodecontentref_/10).
    - [question_id](http://_vscodecontentref_/11): Integer.
    - [answer](http://_vscodecontentref_/12): String.
    - [is_correct](http://_vscodecontentref_/13): Boolean.
    - [timestamp](http://_vscodecontentref_/14): DateTime, default is the current time.

## How to Use

1. **Register a Participant**: Go to `/register` and enter a username to register a new participant.
2. **Take a Quiz**: After registering, you will be redirected to `/quiz/<username>` where you can take the quiz.
3. **Submit Quiz Results**: The quiz results are submitted via a POST request to `/submit`.
4. **View Results**: Go to `/results` and enter the username to view the results.
5. **Admin Statistics**: Go to `/admin/stats` to view statistics (authentication should be added for admin access).
6. **API Statistics**: Access `/api/stats` to get statistics in JSON format.

## Notes

- Ensure that the SQLite database file (`quiz.db`) is created and accessible.
- The application is currently running in debug mode. Do not use it in a production deployment. Use a production WSGI server instead.

## License

This project is licensed under the MIT License.
