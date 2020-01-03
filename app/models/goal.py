from datetime import datetime
from flask import url_for
from app.exceptions import ValidationError
from .. import db


class Goal(db.Model):
    __tablename__ = 'goals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # comments = db.relationship('Comment', backref='post', lazy='dynamic')

    # @staticmethod
    # def on_changed_description(target, value, oldvalue, initiator):
    #     target.description = value

    def to_json(self):
        json_goal = {
            'url': url_for('api.get_goal', id=self.id),
            'name': self.name,
            'description': self.description,
            'timestamp': self.timestamp,
            'author_url': url_for('api.get_user', id=self.author_id),
            # 'comments_url': url_for('api.get_goal_comments', id=self.id),
            # 'comment_count': self.comments.count()
        }
        return json_goal

    @staticmethod
    def from_json(json_post):
        name = json_post.get('name')
        description = json_post.get('description')
        if name is None or name == '':
            raise ValidationError('goal does not have a name')
        return Goal(name=name, description=description)


# db.event.listen(Goal.description, 'set', Goal.on_changed_description)
