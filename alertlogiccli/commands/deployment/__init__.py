from . import mode
from . import status
from . import resources
from . import scan_queue
from . import subnet
from . import installation
from . import scanner

metadata = {
    "subcommands": [
        mode.GetMode(),
        mode.SetMode(),
        resources.ListDeployed(),
        status.GetStatus(),
        scan_queue.ScanHost(),
        scan_queue.ListScanQueues(),
        subnet.SetSubnet(),
        subnet.GetConfiguration(),
        installation.InstallationStatus(),
        installation.Redeploy(),
        scanner.ScannerEstimation()
    ],
    "name": "deployment",
    "help": "deployment related commands"
}
