from datetime import datetime, timedelta
import enum
from flask import url_for
from .. import db
from sqlalchemy.sql import func


class HabitFrequency(enum.Enum):
    daily = 'daily'
    specified = 'specified'
    per_period = 'per_period'
    repeating = 'repeating'


class DurationType(enum.Enum):
    days = 'days'
    weeks = 'weeks'
    months = 'months'
    years = 'years'


class Habit(db.Model):
    __tablename__ = 'habits'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    completions = db.relationship('Completion', backref='habit', lazy='dynamic')
    frequency = db.Column(db.Enum(HabitFrequency))
    duration_count = db.Column(db.Integer)
    duration_type = db.Column(db.Enum(DurationType))
    successful = db.Column(db.Boolean, default=False)
    starts_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    ends_at = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def to_json(self):
        json_habit = {
            'url': url_for('api.get_habit', id=self.id),
            'name': self.name,
            'description': self.description,
            'owner_url': url_for('api.get_user', id=self.owner_id),
            'completions_url': url_for('api.get_habit_completions', id=self.id),
            'completions_count': self.completions.count()
        }
        return json_habit

    @staticmethod
    def from_json(json_habit):
        return Habit(json_habit)


class Completion(db.Model):
    __tablename__ = 'completions'
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'))
    completed_at = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), index=True, server_default=func.now())

    def to_json(self):
        json_completion = {
            'url': url_for('api.get_completion', id=self.id),
            'habit_url': url_for('api.get_habit', id=self.habit_id),
            'target_time': self.target_time,
            'completion_time': self.completion_time
        }
        return json_completion

    @staticmethod
    def from_json(json_completion):
        return Completion(json_completion)
