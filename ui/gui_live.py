# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, scrolledtext
from core.cognitive_layer.meta_kernel_virtualization import MetaKernel
from core.cognitive_layer.orchestrator import Orchestrator
from core.d_levels.d7_field import Field7D
from core.d_levels.d11_time import Field11D
from core.d_levels.d15_control import Field15D
from core.ephemeral_layer.mig import MIG

field7 = Field7D()
field11 = Field11D()
field15 = Field15D()
mig = MIG()
orchestrator = Orchestrator()

mk = MetaKernel(
    field7=field7,
    field11=field11,
    field15=field15,
    mig=mig,
    orchestrator=orchestrator
)

root = tk.Tk()
root.title("Jarvis-VCOS Live GUI")
root.geometry("900x600")

frame_cmd = ttk.Frame(root)
frame_cmd.pack(fill='x', padx=5, pady=5)

frame_log = ttk.LabelFrame(root, text="Decision Log")
frame_log.pack(fill='both', expand=True, padx=5, pady=5)

frame_snap = ttk.LabelFrame(root, text="Latest Snapshot")
frame_snap.pack(fill='both', expand=True, padx=5, pady=5)

frame_status = ttk.LabelFrame(root, text="D-Level Status")
frame_status.pack(fill='both', expand=True, padx=5, pady=5)

command_entry = ttk.Entry(frame_cmd, width=80)
command_entry.pack(side='left', padx=5, pady=5, fill='x', expand=True)
send_button = ttk.Button(frame_cmd, text="Send Command")
send_button.pack(side='left', padx=5, pady=5)

decision_text = scrolledtext.ScrolledText(frame_log, height=15, state='disabled', bg="#1e1e1e", fg="#00ff00")
decision_text.pack(fill='both', expand=True)

snapshot_text = scrolledtext.ScrolledText(frame_snap, height=8, state='disabled', bg="#1e1e1e", fg="#00ffff")
snapshot_text.pack(fill='both', expand=True)

status_text = scrolledtext.ScrolledText(frame_status, height=5, state='disabled', bg="#1e1e1e", fg="#ffcc00")
status_text.pack(fill='both', expand=True)

def send_command():
    cmd = command_entry.get()
    if not cmd.strip():
        return
    result = mk.process_command(cmd)
    decision_text.config(state='normal')
    decision_text.insert('end', f"Command: {cmd}\nResult: {result.get('result')}\nSteps: {result.get('steps')}\n\n")
    decision_text.see('end')
    decision_text.config(state='disabled')
    snapshot = mk.get_latest_snapshot()
    snapshot_text.config(state='normal')
    snapshot_text.delete('1.0','end')
    snapshot_text.insert('end', f"{snapshot}\n")
    snapshot_text.config(state='disabled')
    update_status()

def update_status():
    status = mk.get_hierarchy_status()
    status_text.config(state='normal')
    status_text.delete('1.0','end')
    for layer, s in status.items():
        status_text.insert('end', f"{layer}: {s}\n")
    status_text.config(state='disabled')

def live_update():
    snapshot = mk.get_latest_snapshot()
    snapshot_text.config(state='normal')
    snapshot_text.delete('1.0','end')
    snapshot_text.insert('end', f"{snapshot}\n")
    snapshot_text.config(state='disabled')
    update_status()
    root.after(2000, live_update)

send_button.config(command=send_command)
command_entry.bind("<Return>", lambda e: send_command())

root.after(2000, live_update)
root.mainloop()
