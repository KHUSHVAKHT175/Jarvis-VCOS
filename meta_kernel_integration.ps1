$path = ".\core\cognitive_layer\meta_kernel_virtualization.py"

(Get-Content $path) -replace 'class MetaKernel:', @"
class MetaKernel:
    def __init__(self, field15=None, field11=None, field7=None, mig=None, orchestrator=None):
        self.field15 = field15
        self.field11 = field11
        self.field7 = field7
        self.mig = mig
        self.orchestrator = orchestrator
        self.decision_log = []
        self.memory_manager = MasterMemory(core=self)
"@ | Set-Content $path -Encoding UTF8

Write-Host "MetaKernel.__init__ обновлён и готов для GUI"
