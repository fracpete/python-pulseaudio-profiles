import argparse
import traceback
from pypulseprofiles.core import pulse_create


def main(args=None):
    """
    Creates a PulseAudio profile in YAML format.
    Use -h to see all options.

    :param args: the command-line arguments to use, uses sys.argv if None
    :type args: list
    """

    parser = argparse.ArgumentParser(
        description='Creates a PulseAudio profile in YAML format.',
        prog="ppp-create")
    parser.add_argument("--config", metavar="NAME_OR_FILE", dest="config", default=None, help="the file to store the profile in, outputs it to stdout if not provided")
    parser.add_argument("--source", metavar="NAME_OR_DESC", dest="source", default=None, help="the specific pulseaudio source to use (name or description), otherwise current default is used")
    parser.add_argument("--source_port", metavar="NAME_OR_DESC", dest="source_port", default=None, help="the specific pulseaudio source port to use (name or description), otherwise currently active one is used")
    parser.add_argument("--sink", metavar="NAME_OR_DESC", dest="sink", default=None, help="the specific pulseaudio sink to use (name or description), otherwise current default is used")
    parser.add_argument("--sink_port", metavar="NAME_OR_DESC", dest="sink_port", default=None, help="the specific pulseaudio sink port to use (name or description), otherwise currently active one is used")
    parser.add_argument("--desc", metavar="DESC", dest="desc", default=None, help="the optional description for this profile")
    parser.add_argument("--volume", action="store_true", dest="volume", help="whether to include the (average) volume across all channels")
    parsed = parser.parse_args(args=args)
    pulse_create(config=parsed.config, source_name=parsed.source, sink_name=parsed.sink,
           source_port=parsed.source_port, sink_port=parsed.sink_port, desc=parsed.desc,
                 volume=parsed.volume)


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
