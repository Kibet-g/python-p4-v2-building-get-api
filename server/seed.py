#!/usr/bin/env python3

from random import randint
from faker import Faker

from app import app
from models import db, Game, Review, User

fake = Faker()

with app.app_context():
    # Clear existing data
    Review.query.delete()
    User.query.delete()
    Game.query.delete()

    # Seed users
    users = [User(name=fake.name()) for _ in range(3)]
    db.session.add_all(users)

    # Seed games
    games = [
        Game(title="Mega Adventure", genre="Survival", platform="Xbox", price=30),
        Game(title="Golf Pro IV", genre="Sports", platform="PlayStation", price=20),
        Game(title="Dance, Dance, Dance", genre="Party", platform="PlayStation", price=7),
    ]
    db.session.add_all(games)

    # Seed reviews
    reviews = [
        Review(score=9, comment="Amazing action", user=users[0], game=games[0]),
        Review(score=2, comment="Boring", user=users[0], game=games[1]),
        Review(score=5, comment="Not enough levels", user=users[1], game=games[0]),
        Review(score=randint(0, 10), comment="Confusing instructions", user=users[2], game=games[2]),
    ]
    db.session.add_all(reviews)

    db.session.commit()
