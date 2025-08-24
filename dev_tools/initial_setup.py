""" This is a dev script to set up the initial database state for development purposes. """

from dev_tools.data_factory import user_factory, branch_factory, category_factory, service_factory
from organization.models import Branch
from services.models import ServiceCounter


def create_initial_users():
    users_data = [
        {"username": "alice", "email": "alice@example.com", "password": "password123"},
        {"username": "bob", "email": "bob@example.com", "password": "password123"},
        {"username": "charlie", "email": "charlie@example.com", "password": "password123"},
    ]
    for data in users_data:
        user = user_factory(**data)
        user.save()

def create_initial_branches():
    branches_data = [
        {"name": "Main Branch", "address": "123 Main St", "phone_number": "1234567890", "email": "main@company.com"},
        {"name": "Downtown Branch", "address": "456 Downtown Ave", "phone_number": "0987654321", "email": "downtown@company.com"},
    ]
    for data in branches_data:
        branch = branch_factory(**data)
        branch.save()

def create_initial_categories_and_services():
    categories_data = [
        {"name": "Accounts", "description": "Bank account related services"},
        {"name": "Loans", "description": "Loan and credit services"},
    ]
    services_data = {
        "Accounts": [
            {"name": "Open Savings Account", "description": "Open a new savings account"},
            {"name": "Close Account", "description": "Close an existing account"},
            {"name": "Account Statement", "description": "Request account statement"},
            {"name": "Withdraw Cash", "description": "Withdraw cash from your account"},
        ],
        "Loans": [
            {"name": "Apply for Personal Loan", "description": "Personal loan application"},
            {"name": "Loan Repayment", "description": "Repay your loan"},
            {"name": "Loan Statement", "description": "Request loan statement"},
        ],
    }

    for cat_data in categories_data:
        category = category_factory(**cat_data)
        category.save()
        for svc_data in services_data[cat_data["name"]]:
            service = service_factory(category=category, **svc_data)
            service.save()

def create_initial_service_counters():
    branch = Branch.objects.first()  # Adjust as needed
    counter_names = [
        "Cash Withdrawal",
        "Account Services",
        "Loan Services"
    ]
    for name in counter_names:
        ServiceCounter.objects.create(name=name, branch=branch)