"""Transaction routes."""
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.forms.transaction_forms import TransactionForm, FilterForm
from app.models.transaction import Transaction
from app.config import Config
from datetime import datetime

bp = Blueprint('transactions', __name__, url_prefix='/transactions')

@bp.route('/')
@login_required
def list_transactions():
    """List all transactions with optional filtering."""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    
    # Convert string dates to date objects for the form
    start_date_obj = None
    end_date_obj = None
    
    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        except ValueError:
            start_date = ''
    
    if end_date:
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            end_date = ''
    
    filter_form = FilterForm(data={
        'category': category,
        'start_date': start_date_obj,
        'end_date': end_date_obj
    })
    
    # Apply filters
    filters = {}
    if category:
        filters['category'] = category
    if start_date:
        filters['start_date'] = start_date
    if end_date:
        filters['end_date'] = end_date
    
    # Get total count for pagination
    total = Transaction.count_by_user(current_user.id, **filters)
    
    # Calculate pagination
    per_page = Config.TRANSACTIONS_PER_PAGE
    total_pages = (total + per_page - 1) // per_page
    offset = (page - 1) * per_page
    
    # Get transactions
    transactions = Transaction.get_by_user(
        current_user.id,
        limit=per_page,
        offset=offset,
        order_by='date DESC, created_at DESC',
        **filters
    )
    
    return render_template(
        'transactions/list.html',
        transactions=transactions,
        filter_form=filter_form,
        page=page,
        total_pages=total_pages,
        category=category,
        start_date=start_date,
        end_date=end_date
    )

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    """Add a new transaction."""
    form = TransactionForm()
    
    if form.validate_on_submit():
        Transaction.create(
            user_id=current_user.id,
            description=form.description.data,
            amount=float(form.amount.data),
            transaction_type=form.transaction_type.data,
            category=form.category.data,
            date=form.date.data
        )
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('transactions.list_transactions'))
    
    return render_template('transactions/form.html', form=form, action='Add')

@bp.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    """Edit an existing transaction."""
    transaction = Transaction.get_by_id(transaction_id)
    
    if not transaction or transaction.user_id != current_user.id:
        abort(404)
    
    form = TransactionForm(obj=transaction)
    
    if form.validate_on_submit():
        transaction.update(
            description=form.description.data,
            amount=float(form.amount.data),
            transaction_type=form.transaction_type.data,
            category=form.category.data,
            date=form.date.data
        )
        flash('Transaction updated successfully!', 'success')
        return redirect(url_for('transactions.list_transactions'))
    
    return render_template(
        'transactions/form.html',
        form=form,
        action='Edit',
        transaction=transaction
    )

@bp.route('/delete/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    """Delete a transaction."""
    transaction = Transaction.get_by_id(transaction_id)
    
    if not transaction or transaction.user_id != current_user.id:
        abort(404)
    
    transaction.delete()
    flash('Transaction deleted successfully!', 'success')
    return redirect(url_for('transactions.list_transactions'))