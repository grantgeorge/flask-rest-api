from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Goal, Permission
from . import api
from .decorators import permission_required
from .errors import forbidden, not_found


@api.route('/goals')
def get_goals():
    page = request.args.get('page', 1, type=int)
    pagination = Goal.query.paginate(
        page, per_page=current_app.config['API_POSTS_PER_PAGE'],
        error_out=False)
    goals = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1)
    return jsonify({
        'goals': [goal.to_json() for goal in goals],
        'prev': prev,
        'next': next,
        'count': pagination.total,
    })


@api.route('/goals/<int:id>')
def get_goal(id):
    goal = Goal.query.get(id)
    if not goal:
        return not_found('Resource not found')
    return jsonify(goal.to_json())


@api.route('/goals', methods=['POST'])
@permission_required(Permission.WRITE)
def new_goal():
    goal = Goal.from_json(request.json)
    goal.author = g.current_user
    db.session.add(goal)
    db.session.commit()
    return jsonify(goal.to_json()), 201, \
        {'Location': url_for('api.get_goal', id=goal.id)}


@api.route('/goals/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE)
def edit_goal(id):
    goal = Goal.query.get_or_404(id)
    if g.current_user != goal.author and \
            not g.current_user.can(Permission.ADMIN):
        return forbidden('Insufficient permissions')
    goal.name = request.json.get('name', goal.name)
    goal.description = request.json.get('description', goal.description)
    db.session.add(goal)
    db.session.commit()
    return jsonify(goal.to_json())


@api.route('/goals/<int:id>', methods=['DELETE'])
@permission_required(Permission.WRITE)
def delete_goal(id):
    goal = Goal.query.get_or_404(id)
    if g.current_user != goal.author and \
            not g.current_user.can(Permission.ADMIN):
        return forbidden('Insufficient permissions')
    db.session.delete(goal)
    db.session.commit()
    return jsonify({'result': True})
