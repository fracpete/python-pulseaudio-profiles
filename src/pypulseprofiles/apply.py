import argparse
import traceback
from pypulseprofiles.core import pulse_apply


def main(args=None):
    """
    Outputs information about the PulseAudio setup.
    Use -h to see all options.

    :param args: the command-line arguments to use, uses sys.argv if None
    :type args: list
    """

    parser = argparse.ArgumentParser(
        description='Applies a PulseAudio profile in YAML format.', prog="ppp-apply")
    parser.add_argument("--config", metavar="NAME_OR_FILE", dest="config", default=None, help="the file (or config name) to load the profile from, outputs it to stdout if not provided")
    parser.add_argument("--volume", action="store_true", dest="volume", help="whether to set the (average) volume across all channels")
    parsed = parser.parse_args(args=args)
    pulse_apply(config=parsed.config, volume=parsed.volume)


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
