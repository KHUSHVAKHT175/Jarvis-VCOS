class Orchestrator:
    def __init__(self, memory=None):
        self.memory = memory

    def execute_task(self, cmd):
        print('Orchestrator executing: ' + cmd)
        return {'status':'executed','cmd':cmd}
