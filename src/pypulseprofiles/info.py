import argparse
import traceback
import yaml
from pypulseprofiles.core import pulse_info, APPLICATION_NAME


def main(args=None):
    """
    Outputs information about the PulseAudio setup.
    Use -h to see all options.

    :param args: the command-line arguments to use, uses sys.argv if None
    :type args: list
    """

    parser = argparse.ArgumentParser(
        description='Outputs PulseAudio information in YAML format',
        prog="ppp-info")
    parser.add_argument("--list_sources", action="store_true", dest="list_sources", help="whether to list all the available source")
    parser.add_argument("--list_sinks", action="store_true", dest="list_sinks", help="whether to list all the available sinks")
    parser.add_argument("--volume", action="store_true", dest="volume", help="whether to include the (average) volume across all channels")
    parser.add_argument("--verbose", action="store_true", dest="verbose", help="whether to be more verbose in the output")
    parsed = parser.parse_args(args=args)
    print(yaml.dump(pulse_info(list_sources=parsed.list_sources, list_sinks=parsed.list_sinks,
                               volume=parsed.volume, verbose=parsed.verbose)))


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
