class UserProfile:
    def __init__(self, username):
        self.username = username
        self.days_in_bot = 0
        self.compliments_received = 0
        self.created_notes = 0
        self.other_metrics = {}

    def update_days_in_bot(self, days):
        self.days_in_bot += days

    def add_compliment(self):
        self.compliments_received += 1

    def add_created_note(self):
        self.created_notes += 1

    def update_other_metrics(self, key, value):
        self.other_metrics[key] = value

    def display_profile(self):
        profile_info = f"User: {self.username}\n" 
        profile_info += f"Days in Bot: {self.days_in_bot}\n" 
        profile_info += f"Compliments Received: {self.compliments_received}\n" 
        profile_info += f"Created Notes: {self.created_notes}\n" 
        profile_info += f"Other Metrics: {self.other_metrics}\n" 
        return profile_info

# Example usage
if __name__ == '__main__':
    user_profile = UserProfile('Ajdkckckck')
    user_profile.update_days_in_bot(5)  # Example increment
    user_profile.add_compliment()  # Example increment
    print(user_profile.display_profile())