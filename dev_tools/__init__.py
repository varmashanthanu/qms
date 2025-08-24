from .initial_setup import (
    create_initial_users,
    create_initial_branches,
    create_initial_categories_and_services,
    create_initial_service_counters
)
from .data_factory import (
    user_factory,
    branch_factory,
    category_factory,
    service_factory
)

def run_initial_setup():
    """
    Run the initial setup for development purposes.
    This will create initial users, branches, categories, services, and service counters.
    """
    create_initial_users()
    create_initial_branches()
    create_initial_categories_and_services()
    create_initial_service_counters()
    print("Initial setup completed successfully.")

def reset_database():
    """
    Reset the database to a clean state.
    WARNING: This will delete all data in the database.
    """
    from django.core.management import call_command
    call_command('flush', '--noinput')
    print("Database reset completed successfully.")

def create_super_user(username: str = 'qms_root', email: str = 'root@qms.com', password: str = 'qms_root'):
    """
    Create a superuser for admin access.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Superuser '{username}' created successfully.")
    else:
        print(f"Superuser '{username}' already exists.")