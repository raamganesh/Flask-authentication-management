from flask import Blueprint, render_template, Response, request
from flask_login import login_required, current_user
from . import db
from .data_model import Insight

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/profile")
@login_required
def profile():
    """Render template for profile
    """
    return render_template("profile.html")

@main.route("/profile", methods=["GET", "POST"])
@login_required
def profile_post():
    """POST method to get request from customer to return requested data on profile detail page
        """
    slug = request.form.get("text")
    data = Insight.query.filter_by(slug=slug).first()

    return render_template(
        "profile_detail.html",
        symbol=data.symbol,
        num_market_pairs=data.num_market_pairs,
        date_added=data.date_added,
        cmc_rank=data.cmc_rank,
        last_updated=data.last_updated,
        quote_GBP_price=data.quote_GBP_price,
        quote_GBP_volume_24h=data.quote_GBP_volume_24h,
        quote_GBP_volume_change_24h=data.quote_GBP_volume_change_24h,
        quote_GBP_percent_change_1h=data.quote_GBP_percent_change_1h,
        quote_GBP_percent_change_24h=data.quote_GBP_percent_change_24h)