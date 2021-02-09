import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def get_paginated_questions(request, questions):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  formatted_questions = [question.format() for question in questions]
  return formatted_questions[start:end]


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  
  
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response


  @app.route('/categories')
  def get_categories():

    categories = Category.query.all()
    formatted_categories = {c.id: c.type for c in categories}

    if len(formatted_categories) == 0:
      abort(404)

    else:
      return jsonify({
        'success': True,
        'categories': formatted_categories
      })



  @app.route('/questions')
  def get_questions():

    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = Question.query.all()
    formatted_questions = get_paginated_questions(request, questions)
    categories = Category.query.all()
    formatted_categories = {c.id: c.type for c in categories}

    if len(formatted_questions) == 0:
      abort(404)

    else:
      return jsonify({
        'success': True,
        'questions': formatted_questions,
        'total_questions': len(formatted_questions),
        'current_category': None,
        'categories': formatted_categories
      })


  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):

    question = Question.query.filter(Question.id == question_id).one_or_none()

    if question is None:
      abort(404)

    else:
      question.delete()

      return jsonify({
        'success': True,
        'deleted': question.id
      })


  @app.route('/questions', methods=['POST'])
  def add_question():

    body = request.get_json()

    question = body.get('question', None)
    answer = body.get('answer', None)
    difficulty = body.get('difficulty', None)
    category = body.get('category', None)

    if (question is None) or (answer is None) or (difficulty is None) or (category is None):
      abort(400)

    new_question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
    new_question.insert()

    return jsonify({
      'success': True
    })



  @app.route('/questions/search', methods=['POST'])
  def search_questions():

    body = request.get_json()
    search_term = body.get('searchTerm', '')

    question_results = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
    formatted_questions = get_paginated_questions(request, question_results)

    return jsonify({
      'success': True,
      'questions': formatted_questions,
      'total_questions': len(formatted_questions)
    })

 
  
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):

    category = Category.query.filter_by(id=category_id).one_or_none()

    if category is None:
      abort(404)

    questions = Question.query.filter_by(category=category.id).all()
    formatted_questions = [question.format() for question in questions]

    if len(formatted_questions) == 0:
      abort(404)

    else:
      return jsonify({
        'success': True,
        'questions': formatted_questions,
        'total_questions': len(formatted_questions),
        'current_category': category.type
      })

 
  @app.route('/quizzes', methods=['POST'])
  def get_quiz_question():
    
    body = request.get_json()
    previous_questions = body.get('previous_questions', None)
    category = body.get('quiz_category', None)
    
    if (category is None):
      abort(404)
    
    if category['id'] == 0:
      questions = Question.query.all()

    else:
      questions = Question.query.filter_by(category=category['id']).all()

    valid_questions = [question for question in questions if question.id not in previous_questions]
    formatted_questions = [q.format() for q in valid_questions]

    i = random.randint(0, (len(valid_questions) - 1))
    question = formatted_questions[i]

    return jsonify({
      'success': True,
      'question': question
    })



  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Not Found'
    }), 404

  @app.errorhandler(422)
  def not_processable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'Not able to process request'
    })

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'Bad Request'
    }), 400

  @app.errorhandler(500)
  def internal_error(error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': 'Internal Server Error'
    }), 500
  
  return app

    