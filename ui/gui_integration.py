import tkinter as tk
from core.cognitive_layer.meta_kernel_virtualization import MetaKernel
from core.cognitive_layer.orchestrator import Orchestrator

# РРЅРёС†РёР°Р»РёР·Р°С†РёСЏ СЏРґСЂР° Рё Orchestrator
mk = MetaKernel()
orch = Orchestrator()
mk.orchestrator = orch

# GUI
class JarvisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Jarvis-VCOS Control Panel')

        self.cmd_label = tk.Label(root, text='Enter Command:')
        self.cmd_label.pack()
        self.cmd_entry = tk.Entry(root, width=50)
        self.cmd_entry.pack()

        self.run_button = tk.Button(root, text='Execute', command=self.run_command)
        self.run_button.pack()

        self.log_text = tk.Text(root, height=20, width=80)
        self.log_text.pack()

        self.snapshot_text = tk.Text(root, height=5, width=80)
        self.snapshot_text.pack()

    def run_command(self):
        cmd = self.cmd_entry.get()
        if not cmd: 
            return
        result = mk.process_command(cmd)
        self.log_text.insert(tk.END, f"Command: {cmd}\nResult: {result['result']}\nSteps: {result['steps']}\n\n")
        snapshot = mk.get_latest_snapshot()
        self.snapshot_text.delete('1.0', tk.END)
        self.snapshot_text.insert(tk.END, f"Latest Snapshot:\n{snapshot}")

# Р—Р°РїСѓСЃРє GUI
root = tk.Tk()
app = JarvisGUI(root)
root.mainloop()
