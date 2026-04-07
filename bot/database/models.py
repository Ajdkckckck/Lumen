class UserProfile:
    def __init__(self, username, created_at, last_login, stats=None):
        self.username = username  # User's login
        self.created_at = created_at  # Account creation date
        self.last_login = last_login  # Last login timestamp
        self.stats = stats if stats is not None else {}  # Metrics and statistics

    def update_stats(self, new_stats):
        self.stats.update(new_stats)  # Update user statistics

    def get_metrics(self):
        return self.stats  # Return user metrics

# Example instantiation
user_profile = UserProfile(
    username='Ajdkckckck',
    created_at='2026-04-07 18:51:45',
    last_login='2026-04-07 18:51:45'
)
