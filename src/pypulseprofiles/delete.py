import argparse
import traceback
from pypulseprofiles.core import pulse_delete, APPLICATION_NAME


def main(args=None):
    """
    Deletes the specified profile.
    Use -h to see all options.

    :param args: the command-line arguments to use, uses sys.argv if None
    :type args: list
    """

    parser = argparse.ArgumentParser(
        description='Deletes the specified profile stored in %s.' % ("$HOME/.config/" + APPLICATION_NAME),
        prog="ppp-rm")
    parser.add_argument("--config", metavar="NAME", dest="config", required=True, help="the config name to delete")
    parsed = parser.parse_args(args=args)
    pulse_delete(parsed.config)


def sys_main():
    """
    Runs the main function using the system cli arguments, and
    returns a system error code.

    :return: 0 for success, 1 for failure.
    :rtype: int
    """

    try:
        main()
        return 0
    except Exception:
        print(traceback.format_exc())
        return 1


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(traceback.format_exc())
