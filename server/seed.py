from faker import Faker
from config import app, db
from models import User, Note

fake = Faker()


def seed():
    print('Clearing existing data...')
    Note.query.delete()
    User.query.delete()
    db.session.commit()

    print('Seeding users...')
    users = []
    for _ in range(5):
        user = User(username=fake.unique.user_name())
        user.password_hash = 'password123'
        users.append(user)
        db.session.add(user)

    db.session.commit()

    print('Seeding notes...')
    for user in users:
        for _ in range(fake.random_int(min=3, max=8)):
            note = Note(
                title=fake.sentence(nb_words=5).rstrip('.'),
                content=fake.paragraph(nb_sentences=4),
                user_id=user.id,
            )
            db.session.add(note)

    db.session.commit()
    print(f'Done — seeded {len(users)} users and their notes.')


if __name__ == '__main__':
    with app.app_context():
        seed()
