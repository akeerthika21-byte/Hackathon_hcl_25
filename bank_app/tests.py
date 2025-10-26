from django.test import TestCase
import pytest
from django.urls import reverse
# Create your tests here.
@pytest.mark.django_db
class TestBankAccountView:
    def test_create_account_success(self, create_user_and_login, customer):
        user, api_client = create_user_and_login

        url = reverse('accounts/create/')
        data = {
            "customer_id": customer.Customer_id,
            "account_type": "savings",
            "initial_deposit": "2000.00",
            "branch_name": "Chennai"
        }

        response = api_client.post(url, data, format='json')
        assert response.status_code == 200
        assert "account_number" in response.data
        assert "account_type" in response.data
        assert "balance" in response.data
        assert "branch_name" in response.data
        assert response.data["message"] == "Account created successfully."

    def test_invalid_customer_id(self, create_user_and_login):
        user, api_client = create_user_and_login
        url = reverse('accounts/create/')
        data = {
            "customer_id": "abc",
            "account_type": "savings",
            "initial_deposit": "1500",
            "branch_name": "Chennai"
        }

        response = api_client.post(url, data, format='json')
        assert response.status_code == 400
        assert response.data["error"] == "Invalid customer ID."

    def test_customer_not_found(self, create_user_and_login):
        user, api_client = create_user_and_login
        url = reverse('accounts/create/')
        data = {
            "customer_id": 999,
            "account_type": "savings",
            "initial_deposit": "1500",
            "branch_name": "Chennai"
        }

        response = api_client.post(url, data, format='json')
        assert response.status_code == 404
        assert response.data["error"] == "Customer not found"

    def test_invalid_account_type(self, create_user_and_login, customer):
        user, api_client = create_user_and_login
        url = reverse('accounts/create/')
        data = {
            "customer_id": customer.Customer_id,
            "account_type": "gold",
            "initial_deposit": "1500",
            "branch_name": "Chennai"
        }

        response = api_client.post(url, data, format='json')
        assert response.status_code == 400
        assert response.data["error"] == "Invalid account type"

    def test_minimum_deposit(self, create_user_and_login, customer):
        user, api_client = create_user_and_login
        url = reverse('accounts/create/')
        data = {
            "customer_id": customer.Customer_id,
            "account_type": "savings",
            "initial_deposit": "500",
            "branch_name": "Chennai"
        }

        response = api_client.post(url, data, format='json')
        assert response.status_code == 400
        assert response.data["error"] == "Minimum initial deposit is ₹1000.00."





