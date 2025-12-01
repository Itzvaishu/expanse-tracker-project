from sqlalchemy.orm import Session
from sqlalchemy import func, extract, or_
from datetime import datetime
from app.models import Expense, Transfer, Category

# ================= EXPENSE REPORTS =================

def get_monthly_expense_report(db: Session, user):
    """
    Calculates total expenses (debit) for the current month.
    """
    current_month = datetime.now().month
    current_year = datetime.now().year

    total = db.query(func.sum(Expense.debit)).filter(
        Expense.user_id == user.id,
        extract('month', Expense.created_at) == current_month,
        extract('year', Expense.created_at) == current_year
    ).scalar()

    return total if total is not None else 0.0

def get_recent_expenses(db: Session, user, limit: int = 5):
    """
    Returns latest expenses list.
    """
    return db.query(Expense).filter(
        Expense.user_id == user.id
    ).order_by(Expense.created_at.desc()).limit(limit).all()


# ================= TRANSFER (INCOME) REPORTS =================

def get_monthly_transfers(db: Session, user):
    """
    Calculates total Income for the current month.
    Checks if user is Sender OR Receiver (P2P Logic).
    """
    current_month = datetime.now().month
    current_year = datetime.now().year

    total = db.query(func.sum(Transfer.amount)).filter(
        or_(Transfer.sender_id == user.id, Transfer.receiver_id == user.id),
        extract('month', Transfer.created_at) == current_month,
        extract('year', Transfer.created_at) == current_year
    ).scalar()

    return total if total is not None else 0.0

def get_recent_transfers(db: Session, user, limit: int = 5):
    """
    Returns latest transfers list where user is involved.
    """
    return db.query(Transfer).filter(
        or_(Transfer.sender_id == user.id, Transfer.receiver_id == user.id)
    ).order_by(Transfer.created_at.desc()).limit(limit).all()


# ================= CATEGORY REPORTS =================
# app/services/report_service.py

# Import 'or_' zaroor karein


'''def get_user_categories(db: Session, user):
    """
    Fetches categories based on role.
    - Admin: Sees ALL categories.
    - User: Sees Global Categories (user_id=None) + Their Own Private Categories.
    """
    
    # 1. Agar Admin hai, toh SAB KUCH dikhao
    if user.role.name == "admin":
        categories = db.query(Category).all()
    
    # 2. Agar Normal User hai, toh (Global OR Private) dikhao
    else:
        categories = db.query(Category).filter(
            or_(
                Category.user_id == None,    # Global (Public)
                Category.user_id == user.id  # Private (My Own)
            )
        ).all()
    
    # Frontend ke liye dummy count add karna
    results = []
    for cat in categories:
        cat.count = 0 
        results.append(cat)
        
    return results'''


# app/services/report_service.py

from sqlalchemy import or_ # <--- Yeh zaroori hai

def get_user_categories(db: Session, user):
    
    # Agar Admin hai, toh sab dikhao
    if user.role.name == "admin":
        categories = db.query(Category).all()
    
    # Agar Normal User hai: Global (NULL) + Apni (User ID) dikhao
    else:
        categories = db.query(Category).filter(
            or_(
                Category.user_id == None,    # <--- YEH LINE ZAROORI HAI (Global)
                Category.user_id == user.id  # <--- YEH LINE (Personal)
            )
        ).all()
    
    # Dummy count logic
    results = []
    for cat in categories:
        cat.count = 0 
        results.append(cat)
        
    return results





'''def get_user_categories(db: Session, user):
    """
    Fetches categories for the user.
    """
    categories = db.query(Category).filter(Category.user_id == user.id).all()
    
    results = []
    for cat in categories:
        # Frontend ke liye dummy count, baad mein real logic lagayenge
        cat.count = 0 
        results.append(cat)
        
    return results'''

def get_category_pie_data(db: Session, user):
    """
    Returns data for Pie Chart: Labels (Category Names) and Data (Total Amounts).
    """
    # SQL Query: Join Expense and Category tables, Group by Category Name
    results = db.query(Category.name, func.sum(Expense.debit))\
        .join(Expense, Category.id == Expense.category_id)\
        .filter(Expense.user_id == user.id)\
        .group_by(Category.name)\
        .all()
    
    labels = []
    data = []
    
    for name, total in results:
        labels.append(name)
        data.append(total)
        
    return labels, data

# app/services/report_service.py

# --- PAGINATION LOGIC ---

def get_paginated_expenses(db: Session, user, page: int = 1, page_size: int = 10):
    skip = (page - 1) * page_size
    return db.query(Expense).filter(Expense.user_id == user.id)\
             .order_by(Expense.created_at.desc())\
             .offset(skip).limit(page_size).all()

def get_paginated_transfers(db: Session, user, page: int = 1, page_size: int = 10):
    skip = (page - 1) * page_size
    return db.query(Transfer).filter(
        or_(Transfer.sender_id == user.id, Transfer.receiver_id == user.id)
    ).order_by(Transfer.created_at.desc()).offset(skip).limit(page_size).all()

def get_total_transaction_count(db: Session, user):
    # Total Expense Count
    e_count = db.query(func.count(Expense.id)).filter(Expense.user_id == user.id).scalar()
    # Total Transfer Count
    t_count = db.query(func.count(Transfer.id)).filter(
         or_(Transfer.sender_id == user.id, Transfer.receiver_id == user.id)
    ).scalar()
    
    return e_count + t_count