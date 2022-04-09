from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    """Initiating user table
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))


class Insight(UserMixin, db.Model):
    """Initiating insight table
    """
    __tablename__ = "insight"

    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    symbol = db.Column(db.String(50))
    slug = db.Column(db.String(50))
    num_market_pairs = db.Column(db.Integer)
    date_added = db.Column(db.Date)
    cmc_rank = db.Column(db.Integer)
    last_updated = db.Column(db.Date)
    quote_GBP_price = db.Column(db.Float)
    quote_GBP_volume_24h = db.Column(db.Float)
    quote_GBP_volume_change_24h = db.Column(db.Float)
    quote_GBP_percent_change_1h = db.Column(db.Float)
    quote_GBP_percent_change_24h = db.Column(db.Float)
    sentiment = db.Column(db.Float)
    popularity = db.Column(db.Float)
