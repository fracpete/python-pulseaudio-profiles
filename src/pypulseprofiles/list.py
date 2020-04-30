import argparse
import traceback
from pypulseprofiles.core import pulse_list, APPLICATION_NAME


def main(args=None):
    """
    Lists all the available profiles.
    Use -h to see all options.

    :param args: the command-line arguments to use, uses sys.argv if None
    :type args: list
    """

    parser = argparse.ArgumentParser(
        description='Lists all the available profiles stored in %s.' % ("$HOME/.config/" + APPLICATION_NAME),
        prog="ppp-list")
    parser.add_argument("--verbose", action="store_true", dest="verbose", help="whether to output the content of the profiles as well")
    parsed = parser.parse_args(args=args)
    pulse_list(verbose=parsed.verbose)


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
