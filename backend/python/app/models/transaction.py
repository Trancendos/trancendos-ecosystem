from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class TransactionType(enum.Enum):
    """Enumeration for the type of a financial transaction."""
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    TRANSFER = "TRANSFER"

class Transaction(Base):
    """Represents a single financial transaction in the system.

    Attributes:
        id (int): The unique identifier for the transaction.
        amount (Decimal): The amount of the transaction.
        description (str): A brief description of the transaction.
        type (TransactionType): The type of the transaction (e.g., INCOME, EXPENSE).
        category (str): The category of the transaction (e.g., "Groceries", "Salary").
        user_id (int): The foreign key linking to the user who made the transaction.
        created_at (datetime): The timestamp when the transaction was created.
        updated_at (datetime): The timestamp when the transaction was last updated.
        transaction_date (datetime): The actual date of the transaction.
        reference_number (str): A unique reference number for the transaction.
        user (User): The user object associated with this transaction.
    """
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(precision=19, scale=2), nullable=False)
    description = Column(String(500))
    type = Column(Enum(TransactionType), nullable=False)
    category = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    transaction_date = Column(DateTime, default=datetime.utcnow)
    reference_number = Column(String(100), unique=True)
    
    # Relationships
    user = relationship("User", back_populates="transactions")

class User(Base):
    """Represents a user of the application.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The user's unique username.
        email (str): The user's unique email address.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        created_at (datetime): The timestamp when the user account was created.
        updated_at (datetime): The timestamp when the user account was last updated.
        transactions (List[Transaction]): A list of transactions associated with the user.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="user")