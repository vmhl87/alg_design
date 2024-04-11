# Semi-interactive pretty-printed help dialog

def Help(args):
    # If no additional arguments given, print out summary
    if len(args) == 0:
        print("\033[1m`exit`\033[0m - exit program")
        print("\033[1m`sort`\033[0m - change sorting metric")
        print("\033[1m`add`\033[0m - add state(s) to heap")
        print("\033[1m`pop`\033[0m - remove top state from heap")
        print("\033[1m`reset`\033[0m - reset heap state")
        print("\033[1m`help command`\033[0m - additional information about commands")

    # Give additional information for specific commands
    elif args[0] == "exit":
        print("Usage: \033[1m`exit`\033[0m")
        print("  Exits simulation. Provides a confirmation dialog.")

    elif args[0] == "sort":
        print("Usage: \033[1m`Sort on <metric>`\033[0m\n" +
        "  Can be abbreviated to \033[1m`Sort <metric>`\033[0m, or " +
        "\033[1m`s <metric>`\033[0m")
        print("  By default sorts on population.")
        print("  For a list of available metrics, run \033[1m`Sort list`" +
        "\033[0m.")

    elif args[0] == "add":
        print("Usage: \033[1m`Add <state>`\033[0m")
        print("       \033[1m`Add <region>`\033[0m")
        print("       \033[1m`Add <state1>, <state2>, ...`\033[0m")
        print("  Can be abbreviated to \033[1m`add`\033[0m or \033[1m`a`\033[0m.")
        print("  States are identified by their two-letter abbreviations, in all caps.")
        print("  For a list of valid regions, run \033[1m`Add list`\033[0m.")

    elif args[0] == "pop":
        print("Usage: \033[1m`Pop`\033[0m")
        print("  Can be abbreviated to \033[1m`pop`\033[0m or \033[1m`p`\033[0m.")
        print("  Remove top state from queue, animated.")

    elif args[0] == "reset":
        print("Usage: \033[1m`Reset`\033[0m")
        print("  Can be abbreviated to \033[1m`reset`\033[0m or \033[1m`r`\033[0m.")
        print("  Reset heap state.")

    else:
        print("Information for command \033[1m`" + args[0] + "`\033[0m not found.\n")
        Help([])
