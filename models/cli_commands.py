import argparse

def cli_command_init():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")

    #add
    parser_add = subparser.add_parser("add")
    parser_add.add_argument("--description", required=True)
    parser_add.add_argument("--amount", type=int, required=True)

    # update
    parser_update = subparser.add_parser("update")
    parser_update.add_argument("--id", required=True)
    parser_update.add_argument("--description")
    parser_update.add_argument("--amount", type=int)

    #delete
    parser_delete = subparser.add_parser("delete")
    parser_delete.add_argument("--id", required=True)

    #summary
    parser_summary = subparser.add_parser("summary")
    parser_summary.add_argument("--month", type=int)

    #list
    parser_list = subparser.add_parser("list")

    #clear
    parser_clear = subparser.add_parser("clear")

    return parser