import random
from decimal import Decimal

from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from bank_app.models import Customer, BankAccount, AccountTransaction


class BankAccountView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    def generate_account_no(self):
        # Generate a unique 12-digit account number
        while True:
            acc_no = f"{random.randint(10 ** 11, 10 ** 12 - 1)}"
            if not BankAccount.objects.filter(Account_no=acc_no).exists():
                return acc_no

    def post(self, request):
        # Creates a new bank account for an existing customer
        customer_id = request.data.get('customer_id')
        account_type  = request.data.get('account_type').strip().title()
        initial_deposit = request.data.get('initial_deposit')
        branch_name = request.data.get('branch_name').strip()

        # Validate customer_id
        try:
            customer_id = int(customer_id)
        except ValueError:
            return Response({"error": "Invalid customer ID."}, status=400)

        # Validate required fields
        if not all([customer_id, account_type, initial_deposit, branch_name]):
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate deposit amount
        try:
            initial_deposit = Decimal(initial_deposit)
        except:
            return Response({'error': 'Invalid deposit amount.'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch customer
        try:
            customer_obj = Customer.objects.get(Customer_id=customer_id)
        except Customer.DoesNotExist:
            msg = {
                'error': 'Customer not found',
            }
            return Response(msg, status=status.HTTP_404_NOT_FOUND)

        # Validate account type
        if account_type not in ['Savings', 'Current', 'FD']:
            msg = {
                'error': 'Invalid account type'
            }
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        # Validate minimum deposit
        if initial_deposit < Decimal('1000.00'):
            msg = {
                'error': 'Minimum initial deposit is ₹1000.00.'
            }
            return Response(msg,status=status.HTTP_400_BAD_REQUEST)

        account_no = self.generate_account_no()

        # Creates new account
        with transaction.atomic():
            account = BankAccount.objects.create(Account_no=account_no, Customer_id=customer_obj, Account_type=account_type,
                                                 Branch_name=branch_name, Balance=initial_deposit)
            AccountTransaction.objects.create(Account_id=account, Transaction_type='Credit', Amount=initial_deposit)

            msg = {
            'message': 'Account created successfully.',
            'account_number': account_no,
            'account_type': account_type,
            'balance': str(account.Balance),
            'branch_name': branch_name,
            'created_at': account.Created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            return Response(msg, status=status.HTTP_200_OK)


