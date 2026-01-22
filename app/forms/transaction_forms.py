"""Transaction forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length  
from datetime import date

CATEGORIES = [
    ('salary', 'Salary'),
    ('freelance', 'Freelance'),
    ('investment', 'Investment'),
    ('business', 'Business'),
    ('food', 'Food & Dining'),
    ('transport', 'Transportation'),
    ('utilities', 'Utilities'),
    ('entertainment', 'Entertainment'),
    ('healthcare', 'Healthcare'),
    ('shopping', 'Shopping'),
    ('education', 'Education'),
    ('other', 'Other')
]

class TransactionForm(FlaskForm):
    """Form for adding/editing transactions."""
    description = StringField('Description', validators=[
        DataRequired(),
        Length(min=1, max=200)
    ])
    amount = DecimalField('Amount', validators=[
        DataRequired(),
        NumberRange(min=0.01, message='Amount must be greater than 0')
    ], places=2)
    transaction_type = SelectField('Type', choices=[
        ('income', 'Income'),
        ('expense', 'Expense')
    ], validators=[DataRequired()])
    category = SelectField('Category', choices=CATEGORIES, validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], default=date.today)
    submit = SubmitField('Save Transaction')

class FilterForm(FlaskForm):
    """Form for filtering transactions."""
    category = SelectField('Category', choices=[('', 'All Categories')] + CATEGORIES)
    start_date = DateField('Start Date', validators=[])
    end_date = DateField('End Date', validators=[])
    submit = SubmitField('Apply Filter')