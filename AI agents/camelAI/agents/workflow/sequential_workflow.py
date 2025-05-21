class SequentialWorkflow:
    def __init__(self):
        self.agents = []

    def append(self, agent):
        self.agents.append(agent)

    def run(self):
        data = None
        for agent in self.agents:
            if data is None:
                data = agent.step()
            else:
                data = agent.step(data)
        return data