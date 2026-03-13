from models.tracker_cli import TrackerCLI
from models.cli_commands import cli_command_init

def main():
    parser = cli_command_init()
    args = parser.parse_args()

    cli = TrackerCLI(args)
    cli.process()


if __name__ == "__main__":
    main()