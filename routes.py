from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required
from extensions import db
from models import Task
from flask_cors import cross_origin
import traceback

bp = Blueprint('main', __name__)

@bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Dummy authentication (replace with your authentication logic)
    if username == 'admin' and password == 'password':
        access_token = create_access_token(identity={'username': username})
        return jsonify(access_token=access_token), 200
    return jsonify(message='Invalid credentials'), 401

@bp.route('/tasks', methods=['GET'])
@jwt_required()
@cross_origin()
def get_tasks():
    try:
        tasks = db.session.query(Task).all()
        return jsonify([task.to_dict() for task in tasks])
    except Exception as e:
        current_app.logger.error(f"Error in /tasks GET: {e}\n{traceback.format_exc()}")
        return jsonify(message='Internal server error'), 500

@bp.route('/tasks', methods=['POST'])
@jwt_required()
@cross_origin()
def create_task():
    try:
        data = request.json
        new_task = Task(name=data['name'], description=data.get('description'))
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.to_dict()), 201
    except Exception as e:
        current_app.logger.error(f"Error in /tasks POST: {e}\n{traceback.format_exc()}")
        return jsonify(message='Internal server error'), 500

@bp.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_task(task_id):
    try:
        task = db.session.query(Task).get_or_404(task_id)
        return jsonify(task.to_dict())
    except Exception as e:
        current_app.logger.error(f"Error in /tasks/{task_id} GET: {e}\n{traceback.format_exc()}")
        return jsonify(message='Internal server error'), 500

@bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
@cross_origin()
def update_task(task_id):
    try:
        data = request.json
        task = db.session.query(Task).get_or_404(task_id)
        task.name = data.get('name', task.name)
        task.description = data.get('description', task.description)
        db.session.commit()
        return jsonify(task.to_dict())
    except Exception as e:
        current_app.logger.error(f"Error in /tasks/{task_id} PUT: {e}\n{traceback.format_exc()}")
        return jsonify(message='Internal server error'), 500

@bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
@cross_origin()
def delete_task(task_id):
    try:
        task = db.session.query(Task).get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return '', 204
    except Exception as e:
        current_app.logger.error(f"Error in /tasks/{task_id} DELETE: {e}\n{traceback.format_exc()}")
        return jsonify(message='Internal server error'), 500
