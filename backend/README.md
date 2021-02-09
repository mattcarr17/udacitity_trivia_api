# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## Endpoints

### GET /categories
- Returns a dictionary of all categories with keys 'id' and 'type'. Returns success value.

#### Sample
```curl -X GET http://127.0.0.1:5000/categories```

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

### GET /questions
- Returns all questions, success value, total number of questions returned on page, a list of categories, and ID of current category. 
- Results are paginated. 10 questions per page. Include parameter for page number, default is page 1.
- Error code 404 returned when page number is invalid

#### Sample
```curl -X GET http://127.0.0.1:5000/questions?page=1```

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    ...
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 10
}
```

### GET /categories/<category_id>/questions
- Returns paginated questions of a given category, success value, total questions on page (max 10), and name of category questions belong to.
- Error code 404 returned if page number is invalid

#### Sample
```curl -X GET http://127.0.0.1:5000/categories/1/questions```

```
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
      "answer": "Bear", 
      "category": 1, 
      "difficulty": 1, 
      "id": 32, 
      "question": "Who is the best dog?"
    }
  ], 
  "success": true, 
  "total_questions": 4
}
```

### POST /questions
- Endpoint to create a new question. Takes question, answer, difficulty, and category of question as arguments and inserts new question object into database. 
- Returns success value.
- Error code 400 if request is missing required arguments.

#### Sample
```curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question": "What is the medical name for the heart?", "answer":"myocardium", "difficulty": 3, "category": 1}'```

```
{
  "success": true
}
```

### POST /questions/search
- Returns questions that match passed search term. Returns success value and total number of returned questions.

#### Sample
```curl -X POST http://127.0.0.1:5000/questions/search -H "Content-Type: application/json" -d '{"searchTerm": "lake"}'```

```
{
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

### DELETE /questions/<question_id>
- Deletes a question from database. Returns success value and id of question that was deleted.
- Error code 404 returned if question id was not found in database.

#### Sample
```curl -X DELETE http://127.0.0.1:5000/questions/10```

```
{
  "deleted": 10, 
  "success": true
}
```

### POST /quizzes
- Returns a random question in chosen category that was not in previous questions. Returns success value. 
- If cateogry id is passed as 0, returns random question from any category
- If previous questions is empty, no exclusions to the question returned
- If question returned as null, no more questions in given category
- Error code 404 returned if category is None

#### Sample
```curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"quiz_category": {"type": "History", "id": 4}, "previous_questions": [9]}'```

```
{
  "question": {
    "answer": "Scarab", 
    "category": 4, 
    "difficulty": 4, 
    "id": 23, 
    "question": "Which dung beetle was worshipped by the ancient Egyptians?"
  }, 
  "success": true
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```