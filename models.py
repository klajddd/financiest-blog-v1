from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Concepts(db.Model):
    __tablename__ = "concepts"
    id = db.Column(db.Integer, primary_key=True)
    concept = db.Column(db.String, nullable=False)
    explanation = db.Column(db.String, nullable=False)
