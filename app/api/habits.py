from flask import jsonify, request, g, url_for, current_app
from marshmallow import Schema, fields, ValidationError
from marshmallow_enum import EnumField
from .. import db, ma
from ..models import Habit, Permission
from ..models.habit import HabitFrequency, DurationType
from . import api
from .decorators import permission_required
from .errors import forbidden, not_found, bad_request


def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class HabitSchema(ma.ModelSchema):
    frequency = EnumField(HabitFrequency, by_value=True)
    duration_type = EnumField(DurationType, by_value=True)

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {
            'self': ma.URLFor("api.get_habit", id="<id>"),
            'owner': ma.URLFor("api.get_user", id="<owner_id>"),
            'collection': ma.URLFor("api.get_habits")
        }
    )

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

    class Meta:
        model = Habit


habit_schema = HabitSchema()
habits_schema = HabitSchema(many=True)


@api.route('/habits')
def get_habits():
    page = request.args.get('page', 1, type=int)
    pagination = Habit.query.paginate(
        page, per_page=current_app.config['API_POSTS_PER_PAGE'],
        error_out=False)
    habits = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_habits', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_habits', page=page+1)

    return ({
        'habits': habits_schema.dump(habits),
        'prev': prev,
        'next': next,
        'count': pagination.total,
    })


@api.route('/habits/<int:id>')
def get_habit(id):
    habit = Habit.query.get(id)
    if not habit:
        return not_found('Resource not found.')
    return habit_schema.dump(habit)


@api.route('/habits', methods=['POST'])
@permission_required(Permission.WRITE)
def new_habit():
    json_input = request.get_json()
    try:
        habit = habit_schema.load(json_input)
    except ValidationError as err:
        return bad_request(err.messages)
    habit.owner = g.current_user
    db.session.add(habit)
    db.session.commit()
    return habit_schema.dump(habit)


@api.route('/habits/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE)
def edit_habit(id):
    habit = Habit.query.get_or_404(id)
    if g.current_user != habit.owner and not g.current_user.can(Permission.ADMIN):
        return forbidden('Insufficient permissions.')
    habit.name = request.json.get('name', habit.name)
    habit.description = request.json.get('description', habit.description)
    habit.duration_count = request.json.get('duration_count', habit.duration_count)
    db.session.add(habit)
    db.session.commit()
    return jsonify(habit.to_json())


@api.route('/habits/<int:id>', methods=['DELETE'])
@permission_required(Permission.WRITE)
def delete_habit(id):
    habit = Habit.query.get_or_404(id)
    if g.current_user != habit.owner and not g.current_user.can(Permission.ADMIN):
        return forbidden('Insufficient permissions')
    db.session.delete(habit)
    db.session.commit()
    return jsonify({'result': True})
