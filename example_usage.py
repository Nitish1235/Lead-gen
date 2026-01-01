"""
Example: Programmatic usage of the Lead Discovery System
"""
from main import LeadDiscoveryApp


def example_basic_search():
    """Basic example: Search for businesses in a city"""
    app = LeadDiscoveryApp()
    
    app.start(
        country="United States",
        city="San Francisco",
    )


def example_custom_categories():
    """Example: Search specific categories"""
    app = LeadDiscoveryApp()
    
    app.start(
        country="India",
        city="Mumbai",
        categories=[
            "dental clinic",
            "real estate agency",
            "coaching institute"
        ]
    )


def example_with_stop():
    """Example: Start and stop manually"""
    app = LeadDiscoveryApp()
    
    # Start in background (you'd do this in a separate thread in practice)
    print("Starting discovery...")
    # app.start("United States", "New York")
    
    # Later, stop it
    # app.stop()


if __name__ == "__main__":
    print("Example usage scripts for Lead Discovery System")
    print("Uncomment the function calls below to run examples:")
    print()
    print("# example_basic_search()")
    print("# example_custom_categories()")

