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