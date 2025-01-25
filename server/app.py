# server/app.py

from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    return "Welcome to the Game/Review/User API!"


# Route: Get all games
@app.route('/games', methods=['GET'])
def games():
    games = [game.to_dict() for game in Game.query.all()]
    return make_response(jsonify(games), 200)


# Route: Get a game by ID
@app.route('/games/<int:id>', methods=['GET'])
def game_by_id(id):
    game = Game.query.get(id)
    if not game:
        return make_response({"error": "Game not found"}, 404)

    return make_response(jsonify(game.to_dict()), 200)


# Route: Get all users who reviewed a game
@app.route('/games/users/<int:id>', methods=['GET'])
def game_users_by_id(id):
    game = Game.query.get(id)
    if not game:
        return make_response({"error": "Game not found"}, 404)

    users = [user.to_dict(rules=("-reviews",)) for user in game.users]
    return make_response(jsonify(users), 200)


# Route: Add a review
@app.route('/reviews', methods=['POST'])
def add_review():
    try:
        data = request.get_json()
        review = Review(
            score=data["score"],
            comment=data["comment"],
            game_id=data["game_id"],
            user_id=data["user_id"]
        )
        db.session.add(review)
        db.session.commit()
        return make_response(jsonify(review.to_dict()), 201)
    except Exception as e:
        return make_response({"error": str(e)}, 400)


# Route: Get all users
@app.route('/users', methods=['GET'])
def users():
    users = [user.to_dict() for user in User.query.all()]
    return make_response(jsonify(users), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
