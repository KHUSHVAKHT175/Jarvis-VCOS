from core.cognitive_layer.orchestrator import Orchestrator
from core.d_levels.d7_field import Field7D
from core.d_levels.d11_time import Field11D
from core.d_levels.d15_control import Field15D
from core.ephemeral_layer.mig import MIG
from core.ephemeral_layer.virtual_env import VirtualEnv

# Р—Р°РіР»СѓС€РєР° MasterMemory
class MasterMemory:
    def __init__(self):
        self.store = {}
    def capture_memory(self, cmd, result):
        self.store[cmd] = result

# РРЅС‚РµРіСЂРёСЂРѕРІР°РЅРЅРѕРµ СЏРґСЂРѕ
class MetaKernel:
    def __init__(self):
        self.field7 = Field7D()
        self.field11 = Field11D()
        self.field15 = Field15D()
        self.mig = MIG()
        self.virtual_env = VirtualEnv()
        self.orchestrator = Orchestrator()
        self.memory_manager = MasterMemory()
        self.decision_log = []

    def process_command(self, cmd):
        entry = {'cmd': cmd, 'steps': []}

        # 7D
        ok7, note7 = self.field7.approve_action(cmd)
        entry['steps'].append({'layer': '7D', 'ok': ok7, 'note': note7})
        if not ok7:
            entry['result'] = {'status': 'rejected_7D', 'note': note7}
            self.decision_log.append(entry)
            return entry

        # 11D
        review11 = self.field11.review_action(cmd)
        entry['steps'].append({'layer': '11D', 'review': review11})
        if not review11.get('ok', True):
            entry['result'] = {'status': 'rejected_11D'}
            self.decision_log.append(entry)
            return entry

        # 15D
        final = self.field15.final_approve(cmd, review_summary=review11)
        entry['steps'].append({'layer': '15D', 'final': final})
        if not final.get('ok', True):
            entry['result'] = {'status': 'vetoed_15D'}
            self.decision_log.append(entry)
            return entry

        # I2 execute
        try:
            output = self.mig.flash({'cmd': cmd})
        except Exception:
            output = self.orchestrator.execute_task(cmd)
        entry['result'] = {'status': 'executed', 'output': output}

        # capture to MasterMemory
        self.memory_manager.capture_memory(cmd, entry['result'])

        self.decision_log.append(entry)
        return entry

    def get_decision_log(self, last_n=10):
        return self.decision_log[-last_n:]
