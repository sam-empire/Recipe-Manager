from flask import Blueprint, render_template, redirect, request, url_for
from database import get_db_connection

favorite_bp = Blueprint("favorite", __name__)

@favorite_bp.route("/favorite", methods = ['GET', 'POST'])
def favorite():
    return 1