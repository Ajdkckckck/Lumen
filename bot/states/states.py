from aiogram.fsm.state import State, StatesGroup


class PasswordState(StatesGroup):
    waiting_for_password = State()


class DiaryStates(StatesGroup):
    waiting_password = State()
    waiting_entry = State()


class LettersStates(StatesGroup):
    waiting_password = State()
    # Admin states
    waiting_recipient = State()
    waiting_text = State()


class TimeCapsuleStates(StatesGroup):
    waiting_password = State()
    waiting_message = State()
    waiting_date = State()


class MemoriesStates(StatesGroup):
    waiting_password = State()
    # Admin states
    waiting_text = State()


class SurprisesStates(StatesGroup):
    waiting_password = State()
    # Admin states
    waiting_text = State()
    waiting_surprise_password = State()


class SecretsStates(StatesGroup):
    waiting_password = State()
    waiting_entry = State()


class NotesStates(StatesGroup):
    waiting_text = State()


class MoodStates(StatesGroup):
    waiting_mood = State()


class AchievementsStates(StatesGroup):
    waiting_text = State()


class GoalsStates(StatesGroup):
    waiting_title = State()


class HabitsStates(StatesGroup):
    waiting_name = State()
    waiting_reminder_time = State()


class CareStates(StatesGroup):
    pass


class AdminStates(StatesGroup):
    waiting_compliment = State()
    waiting_support_category = State()
    waiting_support_text = State()
    waiting_care_text = State()
    waiting_morning_text = State()
    waiting_night_text = State()
    waiting_password_section = State()
    waiting_new_password = State()
    waiting_goal_title = State()
    waiting_memory_text = State()
    waiting_letter_text = State()
    waiting_surprise_text = State()
    waiting_surprise_password = State()
