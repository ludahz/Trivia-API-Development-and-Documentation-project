from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy import not_

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    @app.route('/')
    def index():
        return jsonify({
            'message': 'Testing!'
        })

    # Set up CORS. Allow '*' for origins.
    cors = CORS(app, resources={r'*': {'origins': '*'}})

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow', '*'
        )
        return response

    # Endpoint to handle GET requests for all available categories.
    @app.route('/categories')
    def retrieve_categories():
        categories = Category.query.order_by(Category.id).all()
        data = []
        for category in categories:
            data.append({
                "id": category.id,
                "type": category.type
            })
        return jsonify({
            "success": True,
            "categories": data,
            "total_categories": len(Category.query.all()),
        })

    # Endpoint to handle GET requests for questions, including pagination (every 10 questions).
    # This endpoint returns a list of questions,number of total questions, current category, categories.
    @app.route("/questions")
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        categories = Category.query.order_by(Category.id).all()
        current_questions = paginate_questions(request, selection)
        data = []
        for category in categories:
            data.append({
                "id": category.id,
                "type": category.type
            })

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "questions": current_questions,
            "categories": data,
            "total_questions": len(Question.query.all()),
        })

    # GET questions with specific ID
    @app.route('/questions/<int:question_id>', methods=["GET"])
    def retrieve_question_by_id(question_id):
        question = Question.query.filter(
            Question.id == question_id).one_or_none()

        if question is None:
            abort(404)
        else:
            current_category = Category.query.filter(
                Category.id == question.category).all()
            jsonStr = {
                "id": question.id,
                "answer": question.answer,
                "difficulty": question.difficulty,
                "question": question.question,
                "category": current_category[0].type

            }
            return jsonify({
                "success": True,
                "question": jsonStr
            })

    """
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    # Create an endpoint to DELETE question using a question ID.
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                "success": True,
                "deleted": question_id,
                "questions": current_questions,
                "total_questions": len(Question.query.all()),
            })
        except:
            abort(422)

    """
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    # Endpoint to POST a new question,
    # which will require the question and answer text,
    # category, and difficulty score.
    @app.route("/questions", methods=["POST"])
    def post_question():
        body = request.get_json()
        new_question = body.get("question", None)
        answer = body.get("answer", None)
        category = body.get("category", None)
        difficulty = body.get("difficulty", None)
        search = body.get("searchTerm", None)

        """
        TEST: Search by any phrase. The questions list will update to include
        only question that include that string within their question.
        Try using the word "title" to start.
        """
        try:
            # Create a POST endpoint to get questions based on a search term.
            # It should return any questions for whom the search term
            # is a substring of the question.
            if search:
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search))
                )
                current_questions = paginate_questions(request, selection)
                curr_cat_id = current_questions[0]['category']

                current_category = Category.query.filter(
                    Category.id == curr_cat_id).all()

                return jsonify(
                    {
                        "success": True,
                        "questions": current_questions,
                        "total_questions": len(selection.all()),
                        "current_category":  current_category[0].type
                    }
                )

            else:
                if new_question or answer == '':
                    abort(422)
                question = Question(
                    question=new_question, answer=answer, category=category, difficulty=difficulty)
                question.insert()
                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                    "success": True,
                    "created": question.id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all())
                })

        except:
            abort(422)

    """
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

   # Create a GET endpoint to get questions based on category.
    @app.route("/categories/<int:category>/questions")
    def retrieve_question(category):
        selection = Question.query.filter(
            Question.category == category).all()
        current_questions = paginate_questions(request, selection)
        current_category = Category.query.filter(Category.id == category).all()

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(Question.query.all()),
            "current_category": current_category[0].type
        })

    """
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    # POST endpoint to get questions to play the quiz.
    # This endpoint should take category and previous question parameters
    # and return a random questions within the given category,
    # if provided, and that is not one of the previous questions.

    @app.route('/quizzes', methods=['POST'])
    def get_quiz():
        body = request.get_json()
        prevQuestions = body.get('previous_questions')
        quizCategory = body.get('quiz_category')
        question = []
        currentQuest = {}

        if quizCategory['type'] == 'click':
            try:
                n = random.randint(1, 6)
                question = Question.query.filter(
                    Question.category == n).filter(not_(Question.question.in_(prevQuestions))).all()
                if question == []:
                    n = random.randint(1, 6)
                    newQuestion = Question.query.filter(Question.category == n).filter(
                        not_(Question.question.in_(prevQuestions))).all()
                    currentQuest = newQuestion
                else:
                    currentQuest = question
                return jsonify({
                    "success": True,
                    "question": {'id': currentQuest[0].id, 'question': currentQuest[0].question, "answer": currentQuest[0].answer, }
                })
            except:
                abort(404)
        else:
            try:
                if prevQuestions == []:
                    question = Question.query.filter(
                        Question.category == quizCategory['id']).all()
                    n = random.randrange(0, len(question) - 1)
                    currentQuest = question[n]

                else:
                    question = Question.query.filter(
                        Question.category == quizCategory['id']).filter(not_(Question.question.in_(prevQuestions))).all()
                    n = random.randrange(0, len(question))
                    currentQuest = question[n]
                return jsonify({
                    "success": True,
                    "question": {'id': currentQuest.id, 'question': currentQuest.question, "answer": currentQuest.answer, }
                })

            except:
                abort(404)

    """
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    # Create error handlers for all expected errors
    # including 404 and 422.

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                "success": False, "error": 404, "message": "resource not found"
            })
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({
                "success": False, "error": 422, "message": "unprocessable"
            })
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({
                "success": False, "error": 400, "message": "bad request"
            })
        )

    @app.errorhandler(500)
    def internat_server_error(error):
        return (
            jsonify({
                "success": False, "error": 500, "message": "internal server error"
            })
        )

    return app
