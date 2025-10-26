import random

import bcrypt
from django.db import models

# Create your models here.
class Customer(models.Model):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    )

    Customer_id = models.AutoField(primary_key=True)
    First_name = models.CharField(max_length=100)
    Last_name = models.CharField(max_length=100)
    Email = models.EmailField(unique=True)
    Phone_number = models.CharField(max_length=10, unique=True)
    Password = models.CharField(max_length=255)
    Role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    Address = models.CharField(max_length=255, unique=True)
    Aadhar_number = models.CharField(max_length=12, unique=True)
    Pan_number = models.CharField(max_length=12, unique=True)
    Created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        """Hash password using bcrypt."""
        self.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, raw_password):
        """Verify password."""
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))

    class Meta:
        db_table = 'Customer'

class BankAccount(models.Model):
    Account_id = models.AutoField(primary_key=True)
    Account_no = models.CharField(max_length=20, unique=True)
    Customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name="bank_accounts")
    Account_type = models.CharField(max_length=50)
    Branch_name = models.CharField(max_length=100)
    Balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    Status = models.CharField(max_length=20, default="Active")
    Created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'BankAccount'

class AccountTransaction(models.Model):
    Transaction_id = models.AutoField(primary_key=True)
    Account_id = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="transactions")
    Transaction_type = models.CharField(max_length=20)
    Amount = models.DecimalField(max_digits=12, decimal_places=2)
    Transaction_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Transaction'