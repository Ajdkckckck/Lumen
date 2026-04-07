# Updated bot/main.py to add profile router import and registration

# Import the profile router
from routes.profile import profile_router

# Register the profile router in the application
app.include_router(profile_router)