from camel.agents import EmbodiedAgent
from camel.generators import SystemMessageGenerator
from flask import Flask, Response
import threading
import re
from utils.model import get_openai_model

role = "SummaryAgent"
task = "Generate and serve an HTML summary webpage with job and resource data"

agent_spec = dict(role=role, task=task)
agent_msg = SystemMessageGenerator().from_dict(meta_dict=agent_spec)

class SummaryAgent(EmbodiedAgent):
    def __init__(self, model=None):
        if model is None:
            model = get_openai_model()
        super().__init__(
            system_message=agent_msg,
            model=model,
            tool_agents=None,
            code_interpreter=None,
        )
        self.app = Flask(__name__)
        self.html_content = None

        @self.app.route("/")
        def index():
            if self.html_content:
                return Response(self.html_content, mimetype='text/html')
            else:
                return "Page is being generated, please refresh shortly..."

    def step(self, combined_data: dict):
        """
        combined_data:
          - jobs: list of dicts
          - resources: list of dicts
          - preparation_plan: list of dicts or None (optionaly)
        """

        # 1. Generate interview plan via model if not provided
        if "preparation_plan" not in combined_data or not combined_data["preparation_plan"]:
            print("[SummaryAgent] Generating interview plan using model...")
            plan_text = self._generate_interview_plan()
            combined_data["preparation_plan"] = self._parse_plan_text(plan_text)

        # 2. Generate full HTML page via model
        print("[SummaryAgent] Generating HTML webpage using model...")
        html = self._generate_html_page(combined_data)
        self.html_content = html

        # 3. Run Flask server in daemon thread
        thread = threading.Thread(target=self.app.run, kwargs={"debug": False, "use_reloader": False})
        thread.daemon = True
        thread.start()
        
        print("Flask server started at http://127.0.0.1:5000/")
        return {
            "job_positions": combined_data.get("jobs", []),
            "learning_resources": combined_data.get("resources", []),
            "interview_preparation_plan": combined_data.get("preparation_plan", [])
        }

    def _generate_interview_plan(self):
        prompt = (
            "Create a detailed 2-week interview preparation plan for a Python developer job interview. "
            "The plan should include daily goals, a timeline, and resources to learn or review."
            "\nFormat the plan as numbered days with goal and resources."
        )
        response = self.model.chat([{"role": "user", "content": prompt}])
        return response.content

    def _parse_plan_text(self, plan_text):
        """
        Parses the model-generated plan text into a list of dicts
        """
        plan = []
        lines = plan_text.split("\n")
        day_num = 1

        for line in lines:
            if line.strip() == "":
                continue
            # Try to extract day number, goal, resources using regex
            match = re.match(r"(?:Day\s*)?(\d+)[\.\:]\s*(.+)", line, re.I)
            if match:
                day = int(match.group(1))
                rest = match.group(2)
                # Split rest by 'Resources' or 'resources'
                parts = re.split(r"[Rr]esources?[:\-]", rest, maxsplit=1)
                goal = parts[0].strip()
                resources = parts[1].strip() if len(parts) > 1 else ""
                plan.append({"day": day, "goal": goal, "resources": resources})
                day_num = day + 1
            else:
                # fallback: append line as goal without resources
                plan.append({"day": day_num, "goal": line.strip(), "resources": ""})
                day_num += 1
        return plan

    def _generate_html_page(self, data: dict) -> str:
        """
        Use the model to generate the full HTML page content,
        based on jobs, resources, and the interview preparation plan.
        """

        # Prepare content string for prompt
        jobs_str = "\n".join(
            [f"- {job['title']} | Salary: {job['salary']} PLN | Location: {job['location']} | Link: {job['url']}" for job in data.get("jobs", [])]
        ) or "No job positions found."

        resources_str = "\n".join(
            [f"- {res['title']}: {res['href']}" for res in data.get("resources", [])]
        ) or "No resources found."

        plan_str = "\n".join(
            [f"Day {day['day']}: Goal: {day['goal']}. Resources: {day['resources']}" for day in data.get("preparation_plan", [])]
        ) or "No preparation plan available."

        prompt = f"""
                You are an expert Python developer assistant. Generate a clean, simple, and visually pleasant HTML5 webpage that summarizes:

                1. Found job positions, sorted by salary descending, with title, salary, location, and clickable link.
                2. Additional learning resources with clickable links.
                3. A 2-week interview preparation plan, listing daily goals and resources.

                Use semantic HTML and inline CSS styling for clarity and readability. The page title should be 'Python Job Search Summary'.

                Here is the data:

                Jobs:
                {jobs_str}

                Learning Resources:
                {resources_str}

                Interview Preparation Plan:
                {plan_str}

                Return ONLY the full HTML page content.
                """

        response = self.model.chat([{"role": "user", "content": prompt}])
        return response.content
