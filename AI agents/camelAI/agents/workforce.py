from agents.preference_agent import PreferenceAgent
from agents.job_search_agent import JobSearchAgent
from agents.web_agent import WebAgent
from agents.coding_agent import SummaryAgent
from workflow.sequential_workflow import SequentialWorkflow

class JobSearchWorkforce:
    def __init__(self):
        # Create the workflow and add agents in the proper order
        self.workflow = SequentialWorkflow()

        self.pref_agent = PreferenceAgent()
        self.job_agent = JobSearchAgent()
        self.web_agent = WebAgent()
        self.summary_agent = SummaryAgent()

        # Add agents sequentially
        self.workflow.append(self.pref_agent)
        self.workflow.append(self.job_agent)
        self.workflow.append(self.web_agent)
        self.workflow.append(self.summary_agent)

    def run(self):
        return self.workflow.run()
