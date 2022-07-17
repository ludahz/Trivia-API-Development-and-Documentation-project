# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a list of categories objects
- each object has `id` and `type` keys with values corresponding `integer` of `id` and `string` of `type`
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_integer` and `type: category_string` key: value pairs.

```json
{
	"categories": [
		{
			"id": 1,
			"type": "Science"
		},
		{
			"id": 2,
			"type": "Art"
		},
		{
			"id": 3,
			"type": "Geography"
		},
		{
			"id": 4,
			"type": "History"
		},
		{
			"id": 5,
			"type": "Entertainment"
		},
		{
			"id": 6,
			"type": "Sports"
		}
	],
	"success": true,
	"total_categories": 6
}
```

`GET '/api/v1.0/questions`

- Fetches an object with categories and questions keys
- `categories` key contains list of catogry objects with `id` and `type` keys.
- `questions` key contains list of question objects with `answer`, `difficulty`, `category`, `id` and `question` keys
- Request Arguments: None
- Returns: An object with `categories` key with list of objects value,
  - `questions` key with a list of objects value,
  - `success` key with a value of coressponding result i.e `true` of `false`,
  - `total_questions` key with a value of coressponding total number of questions,

```json
{
	"categories": [
		{
			"id": 1,
			"type": "Science"
		},
		{
			"id": 2,
			"type": "Art"
		},
		{
			"id": 3,
			"type": "Geography"
		},
		{
			"id": 4,
			"type": "History"
		},
		{
			"id": 5,
			"type": "Entertainment"
		},
		{
			"id": 6,
			"type": "Sports"
		}
	],
	"questions": [
		{
			"answer": "Tom Cruise",
			"category": 5,
			"difficulty": 4,
			"id": 4,
			"question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
		},
		{
			"answer": "Maya Angelou",
			"category": 4,
			"difficulty": 2,
			"id": 5,
			"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
		},
		{
			"answer": "Edward Scissorhands",
			"category": 5,
			"difficulty": 3,
			"id": 6,
			"question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
		},
		{
			"answer": "Muhammad Ali",
			"category": 4,
			"difficulty": 1,
			"id": 9,
			"question": "What boxer's original name is Cassius Clay?"
		}
	],
	"success": true,
	"total_questions": 26
}
```

`POST '/api/v1.0/questions`

- Creates a new question
- Request Arguments: `question`, `answer`, `category`, `difficulty`
- Returns: An object with `created` key with value of `id` for the created question,
  - `questions` key with a value of list of question objects,
  - `success` key with a value of coressponding result i.e `true` of `false`,
  - `total_questions` key with a value of integer number of available questions.

```json
{
	"created": 42,
	"questions": [
		{
			"answer": "Tom Cruise",
			"category": 5,
			"difficulty": 4,
			"id": 4,
			"question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
		},
		{
			"answer": "Maya Angelou",
			"category": 4,
			"difficulty": 2,
			"id": 5,
			"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
		},
		{
			"answer": "Edward Scissorhands",
			"category": 5,
			"difficulty": 3,
			"id": 6,
			"question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
		},
		{
			"answer": "Muhammad Ali",
			"category": 4,
			"difficulty": 1,
			"id": 9,
			"question": "What boxer's original name is Cassius Clay?"
		},
		{
			"answer": "Brazil",
			"category": 6,
			"difficulty": 3,
			"id": 10,
			"question": "Which is the only team to play in every soccer World Cup tournament?"
		}
	],
	"success": true,
	"total_questions": 26
}
```

`GET '/api/v1.0/questions/${question_id}'`

- Fetches an object of a single question based on the question `id`
- Request Arguments: None
- Returns: An object with `question` key with an object value of the question,
  - `success` key with a value of coressponding result i.e `true` of `false`,

```json
{
	"question": {
		"answer": "Tom Cruise",
		"category": "Entertainment",
		"difficulty": 4,
		"id": 4,
		"question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
	},
	"success": true
}
```

`DELETE '/api/v1.0/questions/${question_id}'`

- Deletes a question based on the given question `id`
- Request Arguments: None
- Returns: An object with `deleted` key with a value of corresponding id of the deleted question,
  - `questions` key with a value of list of question objects,
  - `success` key with a value of coressponding result i.e `true` of `false`,
  - `total_questions` key with a value of integer number of available questions.

```json
{
	"deleted": 12,
	"questions": [
		{
			"answer": "Tom Cruise",
			"category": 5,
			"difficulty": 4,
			"id": 4,
			"question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
		},
		{
			"answer": "Maya Angelou",
			"category": 4,
			"difficulty": 2,
			"id": 5,
			"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
		},
		{
			"answer": "Edward Scissorhands",
			"category": 5,
			"difficulty": 3,
			"id": 6,
			"question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
		},
		{
			"answer": "Muhammad Ali",
			"category": 4,
			"difficulty": 1,
			"id": 9,
			"question": "What boxer's original name is Cassius Clay?"
		},
		{
			"answer": "Brazil",
			"category": 6,
			"difficulty": 3,
			"id": 10,
			"question": "Which is the only team to play in every soccer World Cup tournament?"
		}
	],
	"success": true,
	"total_questions": 25
}
```

`GET '/api/v1.0/categories/${category_id}/questions'`

- Fetches a list of questions based on the category selected.
- Request Arguments: None
- Returns: An object with `current_category` key with a string value of the name of the `category`,
  - `questions` key with a value of list of question objects belonging to the category,
  - `success` key with a value of coressponding result i.e `true` of `false`,
  - `total_questions` key with a value of integer number of available questions.

```json
{
	"current_category": "Science",
	"questions": [
		{
			"answer": "The Liver",
			"category": 1,
			"difficulty": 4,
			"id": 20,
			"question": "What is the heaviest organ in the human body?"
		},
		{
			"answer": "Alexander Fleming",
			"category": 1,
			"difficulty": 3,
			"id": 21,
			"question": "Who discovered penicillin?"
		},
		{
			"answer": "Blood",
			"category": 1,
			"difficulty": 4,
			"id": 22,
			"question": "Hematology is a branch of medicine involving the study of what?"
		},
		{
			"answer": "science Answer",
			"category": 1,
			"difficulty": 1,
			"id": 40,
			"question": "Science question?"
		}
	],
	"success": true,
	"total_questions": 26
}
```

`POST '/api/v1.0/quizzes'`

- Fetches a random question based on the category selected.
- Request Arguments:

```json
{
	"previous_questions": ["Who discovered penicillin?"],
	"quiz_category": {
		"type": "Science",
		"id": 1
	}
}
```

- Returns: An object with `question` key with an object value,
  - `success` key with a value of coressponding result i.e `true` of `false`,

```json
{
	"question": {
		"answer": "Blood",
		"id": 22,
		"question": "Hematology is a branch of medicine involving the study of what?"
	},
	"success": true
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
