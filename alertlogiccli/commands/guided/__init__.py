from . import subnet
from . import installation
from . import scanner

metadata = {
    "subcommands": [
        subnet.SetSubnet(),
        subnet.GetConfiguration(),
        installation.InstallationStatus(),
        installation.Redeploy(),
        scanner.ScannerEstimation()
    ],
    "name": "guided",
    "help": "guided mode related commands"
}
