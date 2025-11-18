from core.cognitive_layer.orchestrator import Orchestrator
from core.d_levels.d7_field import Field7D
from core.d_levels.d11_time import Field11D
from core.d_levels.d15_control import Field15D
from core.ephemeral_layer.mig import MIG
from core.ephemeral_layer.virtual_env import VirtualEnv

# MasterMemory с versioning и embedding-защелкой
class MasterMemory:
    def __init__(self):
        self.store = {}      # Основная память
        self.snapshots = []  # Снапшоты истории команд

    def capture_memory(self, cmd, result):
        entry = {'cmd': cmd, 'result': result}
        self.store[cmd] = result
        self.snapshots.append(entry)

    def get_snapshot(self, idx=-1):
        if self.snapshots:
            return self.snapshots[idx]
        return None

# Интегрированное ядро с виртуализацией и снапшотами
class MetaKernel:
    def __init__(self, field7=None, field11=None, field15=None, mig=None, orchestrator=None, virtual_env=None):
        # Поддержка внешних объектов или создание дефолтных
        self.field7 = field7 if field7 else Field7D()
        self.field11 = field11 if field11 else Field11D()
        self.field15 = field15 if field15 else Field15D()
        self.mig = mig if mig else MIG()
        self.virtual_env = virtual_env if virtual_env else VirtualEnv()
        self.orchestrator = orchestrator if orchestrator else Orchestrator()
        self.memory_manager = MasterMemory()
        self.decision_log = []

    def process_command(self, cmd):
        # Создаём виртуальную изолированную копию слоёв
        env = self.virtual_env.clone_layer({
            '7D': self.field7,
            '11D': self.field11,
            '15D': self.field15,
            'MIG': self.mig
        })

        entry = {'cmd': cmd, 'steps': []}

        # 7D быстрый анализ
        ok7, note7 = env['7D'].approve_action(cmd)
        entry['steps'].append({'layer': '7D', 'ok': ok7, 'note': note7})
        if not ok7:
            entry['result'] = {'status': 'rejected_7D', 'note': note7}
            self.decision_log.append(entry)
            return entry

        # 11D глубокий review
        review11 = env['11D'].review_action(cmd)
        entry['steps'].append({'layer': '11D', 'review': review11})
        if not review11.get('ok', True):
            entry['result'] = {'status': 'rejected_11D'}
            self.decision_log.append(entry)
            return entry

        # 15D финальный контроль
        final = env['15D'].final_approve(cmd, review_summary=review11)
        entry['steps'].append({'layer': '15D', 'final': final})
        if not final.get('ok', True):
            entry['result'] = {'status': 'vetoed_15D'}
            self.decision_log.append(entry)
            return entry

        # I2 execute через MIG в виртуальной среде, fallback Orchestrator
        try:
            output = env['MIG'].flash({'cmd': cmd})
        except Exception:
            output = self.orchestrator.execute_task(cmd)
        entry['result'] = {'status': 'executed', 'output': output}

        # Сохраняем снапшот
        self.memory_manager.capture_memory(cmd, entry['result'])

        # Логируем результат
        self.decision_log.append(entry)
        return entry

    def get_decision_log(self, last_n=10):
        return self.decision_log[-last_n:]

    def get_latest_snapshot(self):
        return self.memory_manager.get_snapshot()
