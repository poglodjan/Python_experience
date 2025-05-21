from camel.agents import BaseAgent
from api.linkup_api import LinkupApi  

class JobSearchAgent(BaseAgent):
    """
    Uses the Linkup API wrapper to find jobs based on preferences.
    """
    def __init__(self, name="JobSearchAgent"):
        super().__init__(name=name)
        self.linkup = LinkupApi()

    def step(self, preferences: dict):
        print("=== [JobSearchAgent] Searching for jobs via Linkup API ===")

        query = preferences.get("tech_stack", "Python")
        location = preferences.get("location", "remote")

        try:
            data = self.linkup.search_jobs(query=query, location=location)
        except Exception as e:
            print(f"[JobSearchAgent] API call failed: {e}")
            return []

        jobs = data.get("results", [])
        filtered_jobs = []

        for job in jobs:
            title = job.get("title", "").lower()
            salary = job.get("salary", 0)
            location = job.get("location", "N/A")

            if preferences["position_level"].lower() in title and salary > preferences["min_salary"]:
                filtered_jobs.append({
                    "title": job.get("title"),
                    "salary": salary,
                    "location": location,
                    "url": job.get("url")
                })

        sorted_jobs = sorted(filtered_jobs, key=lambda x: x["salary"], reverse=True)
        print(f"[JobSearchAgent] Found {len(sorted_jobs)} matching jobs.")
        return sorted_jobs
