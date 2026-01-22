"""Main application routes."""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.transaction import Transaction

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Landing page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard showing overview of finances."""
    summary = Transaction.get_summary(current_user.id)
    
    # Get recent transactions
    recent_transactions = Transaction.get_by_user(
        current_user.id,
        limit=5,
        order_by='date DESC, created_at DESC'
    )
    
    return render_template(
        'main/dashboard.html',
        summary=summary,
        recent_transactions=recent_transactions
    )