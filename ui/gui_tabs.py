import tkinter as tk
from tkinter import ttk
from core.cognitive_layer.meta_kernel_virtualization import MetaKernel
from core.cognitive_layer.orchestrator import Orchestrator

# РРЅРёС†РёР°Р»РёР·Р°С†РёСЏ СЏРґСЂР° Рё Orchestrator
mk = MetaKernel()
orch = Orchestrator()
mk.orchestrator = orch

# GUI СЃ РІРєР»Р°РґРєР°РјРё
class JarvisTabsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Jarvis-VCOS Control Panel')

        self.tabControl = ttk.Notebook(root)

        # Р’РєР»Р°РґРєРё
        self.tab_log = ttk.Frame(self.tabControl)
        self.tab_snapshot = ttk.Frame(self.tabControl)
        self.tab_orch = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab_log, text='Decision Log')
        self.tabControl.add(self.tab_snapshot, text='Latest Snapshot')
        self.tabControl.add(self.tab_orch, text='Orchestrator Status')
        self.tabControl.pack(expand=1, fill='both')

        # Decision Log
        self.log_text = tk.Text(self.tab_log, height=20, width=80)
        self.log_text.pack()

        # Latest Snapshot
        self.snapshot_text = tk.Text(self.tab_snapshot, height=20, width=80)
        self.snapshot_text.pack()

        # Orchestrator Status
        self.orch_text = tk.Text(self.tab_orch, height=20, width=80)
        self.orch_text.pack()
        self.update_orchestrator_status()

        # РљРѕРјР°РЅРґРЅР°СЏ РїР°РЅРµР»СЊ
        self.cmd_label = tk.Label(root, text='Enter Command:')
        self.cmd_label.pack()
        self.cmd_entry = tk.Entry(root, width=50)
        self.cmd_entry.pack()
        self.run_button = tk.Button(root, text='Execute', command=self.run_command)
        self.run_button.pack()

    def run_command(self):
        cmd = self.cmd_entry.get()
        if not cmd:
            return
        result = mk.process_command(cmd)
        # РћР±РЅРѕРІР»РµРЅРёРµ РІРєР»Р°РґРєРё Decision Log
        self.log_text.insert(tk.END, f"Command: {cmd}\nResult: {result['result']}\nSteps: {result['steps']}\n\n")
        # РћР±РЅРѕРІР»РµРЅРёРµ РІРєР»Р°РґРєРё Latest Snapshot
        snapshot = mk.get_latest_snapshot()
        self.snapshot_text.delete('1.0', tk.END)
        self.snapshot_text.insert(tk.END, f"Latest Snapshot:\n{snapshot}")
        # РћР±РЅРѕРІР»РµРЅРёРµ Orchestrator Status
        self.update_orchestrator_status()

    def update_orchestrator_status(self):
        self.orch_text.delete('1.0', tk.END)
        status = orch.get_status() if hasattr(orch, 'get_status') else 'Orchestrator ready'
        self.orch_text.insert(tk.END, str(status))

# Р—Р°РїСѓСЃРє GUI
root = tk.Tk()
app = JarvisTabsGUI(root)
root.mainloop()
