from camel.agents import BaseAgent
from hitl.hitl_tool import ask_user_input

class PreferenceAgent(BaseAgent):
    """
    collects user preferences (human-in-loop)
    """
    def __init__(self, name="PreferenceAgent"):
        super().__init__(name=name)

    def step(self, *args, **kwargs):
        print("=== [PreferenceAgent] Collecting Job Preferences ===")

        preferences = {}
        preferences["position_level"] = ask_user_input(
            "Preferred position level (e.g., junior/mid/senior)", default="mid"
        )
        try:
            preferences["min_salary"] = int(ask_user_input(
                "Minimum acceptable salary (PLN)", default="16000"
            ))
        except ValueError:
            preferences["min_salary"] = 16000

        preferences["location"] = ask_user_input(
            "Preferred location (e.g., Warsaw or remote)", default="remote"
        )
        preferences["tech_stack"] = ask_user_input(
            "Preferred tech stack (optional)", default="Python"
        )

        print("\nCollected preferences:")
        for k, v in preferences.items():
            print(f"  - {k}: {v}")

        return preferences
