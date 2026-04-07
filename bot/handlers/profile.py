class ProfileHandler:
    def __init__(self, user_id):
        self.user_id = user_id
        self.user_data = self.get_user_data()

    def get_user_data(self):
        # Simulate fetching user data from the database
        return {
            'days_in_bot': 100,
            'notes_created': 25,
            'diary_entries': 50,
            'achievements': ['Started a habit', 'Completed a project'],
            'habits': {'exercise': 10, 'reading': 15},
            'mood_history': ['happy', 'neutral', 'sad'],
            'goals_stats': {'ongoing': 3, 'completed': 2}
        }

    def display_profile(self):
        # Display the user's profile statistics
        print(f"User ID: {self.user_id}")
        print(f"Days in Bot: {self.user_data['days_in_bot']}")
        print(f"Notes Created: {self.user_data['notes_created']}")
        print(f"Diary Entries: {self.user_data['diary_entries']}")
        print(f"Achievements: {', '.join(self.user_data['achievements'])}")
        print(f"Habits: {self.user_data['habits']}")
        print(f"Mood History: {', '.join(self.user_data['mood_history'])}")
        print(f"Goals Stats: {self.user_data['goals_stats']}")

# Example usage
if __name__ == '__main__':
    profile_handler = ProfileHandler(user_id='user123')
    profile_handler.display_profile()