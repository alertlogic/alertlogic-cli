from . import mode
from . import status
from . import resources
from . import scan_queue

metadata = {
    "subcommands": [
        mode.GetMode(),
        mode.SetMode(),
        resources.ListDeployed(),
        status.GetStatus(),
        scan_queue.ScanHost(),
        scan_queue.ListScanQueues()
    ],
    "name": "deployment",
    "help": "deployment related commands"
}
