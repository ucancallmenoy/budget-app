"""Transaction model."""
from app.models.database import get_db

class Transaction:
    """Transaction model for income and expenses."""
    
    def __init__(self, id, user_id, description, amount, transaction_type, 
                 category, date, created_at=None):
        self.id = id
        self.user_id = user_id
        self.description = description
        self.amount = amount
        self.transaction_type = transaction_type
        self.category = category
        self.date = date
        self.created_at = created_at
    
    @staticmethod
    def create(user_id, description, amount, transaction_type, category, date):
        """Create a new transaction."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO transactions 
                   (user_id, description, amount, transaction_type, category, date) 
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (user_id, description, amount, transaction_type, category, date)
            )
            conn.commit()
            return Transaction.get_by_id(cursor.lastrowid)
    
    @staticmethod
    def get_by_id(transaction_id):
        """Get transaction by ID."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM transactions WHERE id = ?', (transaction_id,))
            row = cursor.fetchone()
            
            if row:
                return Transaction(
                    id=row['id'],
                    user_id=row['user_id'],
                    description=row['description'],
                    amount=row['amount'],
                    transaction_type=row['transaction_type'],
                    category=row['category'],
                    date=row['date'],
                    created_at=row['created_at']
                )
        return None
    
    @staticmethod
    def get_by_user(user_id, limit=None, offset=0, category=None, 
                    start_date=None, end_date=None, order_by='date DESC'):
        """Get transactions for a user with optional filters."""
        with get_db() as conn:
            cursor = conn.cursor()
            
            query = 'SELECT * FROM transactions WHERE user_id = ?'
            params = [user_id]
            
            if category:
                query += ' AND category = ?'
                params.append(category)
            
            if start_date:
                query += ' AND date >= ?'
                params.append(start_date)
            
            if end_date:
                query += ' AND date <= ?'
                params.append(end_date)
            
            query += f' ORDER BY {order_by}'
            
            if limit:
                query += ' LIMIT ? OFFSET ?'
                params.extend([limit, offset])
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            return [Transaction(
                id=row['id'],
                user_id=row['user_id'],
                description=row['description'],
                amount=row['amount'],
                transaction_type=row['transaction_type'],
                category=row['category'],
                date=row['date'],
                created_at=row['created_at']
            ) for row in rows]
    
    @staticmethod
    def count_by_user(user_id, category=None, start_date=None, end_date=None):
        """Count transactions for a user with optional filters."""
        with get_db() as conn:
            cursor = conn.cursor()
            
            query = 'SELECT COUNT(*) as count FROM transactions WHERE user_id = ?'
            params = [user_id]
            
            if category:
                query += ' AND category = ?'
                params.append(category)
            
            if start_date:
                query += ' AND date >= ?'
                params.append(start_date)
            
            if end_date:
                query += ' AND date <= ?'
                params.append(end_date)
            
            cursor.execute(query, params)
            return cursor.fetchone()['count']
    
    def update(self, description, amount, transaction_type, category, date):
        """Update transaction."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''UPDATE transactions 
                   SET description = ?, amount = ?, transaction_type = ?, 
                       category = ?, date = ?
                   WHERE id = ?''',
                (description, amount, transaction_type, category, date, self.id)
            )
            conn.commit()
        
        self.description = description
        self.amount = amount
        self.transaction_type = transaction_type
        self.category = category
        self.date = date
    
    def delete(self):
        """Delete transaction."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM transactions WHERE id = ?', (self.id,))
            conn.commit()
    
    @staticmethod
    def get_summary(user_id):
        """Get income, expense, and balance summary for a user."""
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                '''SELECT 
                   SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END) as total_income,
                   SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) as total_expense
                   FROM transactions WHERE user_id = ?''',
                (user_id,)
            )
            row = cursor.fetchone()
            
            total_income = row['total_income'] or 0
            total_expense = row['total_expense'] or 0
            balance = total_income - total_expense
            
            return {
                'total_income': total_income,
                'total_expense': total_expense,
                'balance': balance
            }