from datetime import datetime, timezone
from sqlalchemy.orm import validates
from config import db, bcrypt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    _password_hash = db.Column(db.String(256), nullable=False)

    notes = db.relationship('Note', back_populates='user', cascade='all, delete-orphan')

    @validates('username')
    def validate_username(self, key, username):
        if not username or len(username.strip()) < 3:
            raise ValueError('Username must be at least 3 characters.')
        return username.strip()

    @property
    def password_hash(self):
        raise AttributeError('Password hash is write-only.')

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
        }

    def __repr__(self):
        return f'<User {self.username}>'


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='notes')

    @validates('title')
    def validate_title(self, key, title):
        if not title or len(title.strip()) == 0:
            raise ValueError('Title cannot be blank.')
        return title.strip()

    @validates('content')
    def validate_content(self, key, content):
        if not content or len(content.strip()) == 0:
            raise ValueError('Content cannot be blank.')
        return content.strip()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user_id': self.user_id,
        }

    def __repr__(self):
        return f'<Note {self.title!r}>'
