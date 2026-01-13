import sqlite3
from datetime import datetime, timedelta

# Database setup
conn = sqlite3.connect("database.db", check_same_thread=False)
cur = conn.cursor()

def init_db():
    # Create table with basic columns if not exists
    cur.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, paid INTEGER DEFAULT 0)")
    
    # Check existing columns
    cur.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cur.fetchall()]
    
    # Rename 'paid' to 'is_paid' if exists
    if 'paid' in columns and 'is_paid' not in columns:
        cur.execute("ALTER TABLE users RENAME COLUMN paid TO is_paid")
        columns = [c if c != 'paid' else 'is_paid' for c in columns]
    
    # Add missing columns
    if 'expiry' not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN expiry TEXT")
    if 'plan_type' not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN plan_type TEXT DEFAULT 'basic'")
    if 'referred_by' not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN referred_by INTEGER")
    if 'referral_count' not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN referral_count INTEGER DEFAULT 0")
    if 'wallet_balance' not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN wallet_balance INTEGER DEFAULT 0")
    if 'upi_id' not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN upi_id TEXT")
    if 'payment_amount' not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN payment_amount INTEGER DEFAULT 0")
    
    conn.commit()

init_db()

def get_user(user_id):
    """Get user data by user_id"""
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    return cur.fetchone()

def add_user(user_id, referred_by=None):
    """Add new user if not exists"""
    if not get_user(user_id):
        cur.execute("INSERT INTO users (user_id, referred_by) VALUES (?, ?)", (user_id, referred_by))
        conn.commit()

def verify_user(user_id, amount):
    """Verify payment and set expiry based on amount"""
    if amount == 49:
        days = 7
    elif amount == 149:
        days = 30
    elif amount == 499:
        days = 365
    else:
        days = 30  # default
    expiry = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
    cur.execute("UPDATE users SET is_paid=1, expiry=?, payment_amount=? WHERE user_id=?", (expiry, amount, user_id))
    conn.commit()

def unverify_user(user_id):
    """Remove access"""
    cur.execute("UPDATE users SET is_paid=0, expiry=NULL WHERE user_id=?", (user_id,))
    conn.commit()

def get_paid_users():
    """Get all paid users"""
    cur.execute("SELECT user_id FROM users WHERE is_paid=1")
    return [row[0] for row in cur.fetchall()]

def get_stats():
    """Get stats: total users, paid users"""
    cur.execute("SELECT COUNT(*) FROM users")
    total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM users WHERE is_paid=1")
    paid = cur.fetchone()[0]
    return total, paid

def update_referral_count(user_id):
    """Increment referral count"""
    cur.execute("UPDATE users SET referral_count = referral_count + 1 WHERE user_id=?", (user_id,))
    conn.commit()

def add_to_wallet(user_id, amount):
    """Add amount to user's wallet"""
    cur.execute("UPDATE users SET wallet_balance = wallet_balance + ? WHERE user_id=?", (amount, user_id))
    conn.commit()

def deduct_from_wallet(user_id, amount):
    """Deduct amount from user's wallet"""
    cur.execute("UPDATE users SET wallet_balance = wallet_balance - ? WHERE user_id=?", (amount, user_id))
    conn.commit()

def set_upi_id(user_id, upi):
    """Set UPI ID for user"""
    cur.execute("UPDATE users SET upi_id=? WHERE user_id=?", (upi, user_id))
    conn.commit()

def check_expiry_reminders():
    """Check users whose expiry is in 2 days and return their ids"""
    two_days_later = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
    cur.execute("SELECT user_id FROM users WHERE is_paid=1 AND expiry=?", (two_days_later,))
    return [row[0] for row in cur.fetchall()]