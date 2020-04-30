import os

APPLICATION_NAME = "python-pulseaudio-profiles"
""" the name of the application and pulseaudio client. """


def config_dir():
    """
    Returns the config directory ($HOME/.config/python-pulseaudio-profiles).

    :return: the directory for the configurations
    :rtype: str
    """

    return os.path.expanduser("~/.config/" + APPLICATION_NAME)


def init_config_dir():
    """
    Ensures that the config directory is present.

    :return: if directory present
    :rtype: bool
    """

    d = config_dir()
    if os.path.exists(d):
        return os.path.isdir(d)
    else:
        os.mkdir(d, mode=0o700)
        return True


def expand_config(file_or_name):
    """
    Expands the configuration file or name.

    :param file_or_name: the file or name (beneath $HOME/.config/python-pulseaudio-profiles)
    :type file_or_name: str
    :return: the absolute file name
    :rtype: str
    """

    root, ext = os.path.splitext(file_or_name)
    head, tail = os.path.split(file_or_name)
    if (ext == "") and (head == ""):
        return os.path.join(config_dir(), tail + ".yaml")
    else:
        return os.path.abspath(os.path.expanduser(file_or_name))


def is_config_name(file_or_name):
    """
    Checks whether the string represents a file or just a config name.

    :param file_or_name: the string to check
    :type file_or_name: str
    :return: whether a config name rather than a filename.
    :rtype: bool
    """

    result = False
    if os.path.commonprefix([expand_config(file_or_name), config_dir()]) == config_dir():
        result = True
    return result


def list_configs():
    """
    Returns the names of all the config files in $HOME/.config/python-pulseaudio-profiles.

    :return: the list of configurations
    :rtype: list
    """

    result = []

    for f in os.listdir(config_dir()):
        if f.endswith(".yaml"):
            result.append(os.path.splitext(f)[0])

    return result

def delete_config(config):
    """
    Deletes the specified configuration.

    :param config: the configuration name
    :type config: str
    """

    if is_config_name(config):
        fname = expand_config(config)
        os.remove(fname)
    else:
        raise Exception("Unknown profile: %s" % config)
