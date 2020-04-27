import os
import pulsectl
import yaml

APPLICATION_NAME = "python-pulseaudio-profiles"
""" the name of the application and pulseaudio client. """


def pulse_instance():
    """
    Returns an Pulse instance.

    :return: the instance
    :rtype: pulsectl.Pulse
    """
    return pulsectl.Pulse(APPLICATION_NAME)


def pulse_source_info(source, verbose=False):
    """
    Generates a dictionary from the PulseSourceInfo object.

    :param source: the PulseSinkInfo object to use
    :type source: pulsectl.PulseSinkInfo
    :param verbose: whether to generate a verbose result
    :type verbose: bool
    :return: dictionary of info
    :rtype: dict
    """

    result = {}

    if verbose:
        result['device'] = {}
        result['device']['name'] = source.name
        result['device']['description'] = source.description
        if source.port_active is not None:
            result['port'] = {}
            result['port']['name'] = source.port_active.name
            result['port']['description'] = source.port_active.description
    else:
        result['device'] = source.description
        if source.port_active is not None:
            result['port'] = source.port_active.description

    return result


def pulse_sink_info(sink, verbose=False):
    """
    Generates a dictionary from the PulseSinkInfo object.

    :param sink: the PulseSinkInfo object to use
    :type sink: pulsectl.PulseSinkInfo
    :param verbose: whether to generate a verbose result
    :type verbose: bool
    :return: dictionary of info
    :rtype: dict
    """

    result = {}

    if verbose:
        result['device'] = {}
        result['device']['name'] = sink.name
        result['device']['description'] = sink.description
        if sink.port_active is not None:
            result['port'] = {}
            result['port']['name'] = sink.port_active.name
            result['port']['description'] = sink.port_active.description
    else:
        result['device'] = sink.description
        if sink.port_active is not None:
            result['port'] = sink.port_active.description

    return result


def pulse_info(list_sources=False, list_sinks=False, verbose=False):
    """
    Returns a dictionary with information about the setup.

    :param list_sources: whether to list sources
    :type list_sources: bool
    :param list_sinks: whether to list sinks
    :type list_sinks: bool
    :param verbose: whether to be verbose
    :type verbose: bool
    """

    pulse = pulse_instance()

    info = dict()
    info['default_source'] = pulse_source_info(pulse_source(), verbose=verbose)
    info['default_sink'] = pulse_sink_info(pulse_sink(), verbose=verbose)

    if list_sources:
        sources = []
        for s in pulse.source_list():
            sources.append(pulse_source_info(s, verbose=verbose))
        info['sources'] = sources

    if list_sinks:
        sinks = []
        for s in pulse.source_list():
            sinks.append(pulse_sink_info(s, verbose=verbose))
        info['sinks'] = sinks

    configs = list_configs()
    if len(configs) > 0:
        info['profiles'] = configs

    return info


def pulse_source(name_or_desc=None):
    """
    Returns the PulseSourceInfo that matches the string, either against the name or the description.

    :param name_or_desc: the name or description string to look for, uses default source if None
    :type name_or_desc: str
    :return: the PulseSourceInfo object or None if not found
    :rtype: pulsectl.PulseSourceInfo
    """

    result = None
    pulse = pulse_instance()

    if name_or_desc is None:
        name_or_desc = pulse.server_info().default_source_name

    for s in pulse.source_list():
        if (s.name == name_or_desc) or (s.description == name_or_desc):
            result = s
            break

    return result


def pulse_sink(name_or_desc=None):
    """
    Returns the PulseSinkInfo that matches the string, either against the name or the description.

    :param name_or_desc: the name or description string to look for, uses default sink if None
    :type name_or_desc: str
    :return: the PulseSinkInfo object or None if not found
    :rtype: pulsectl.PulseSinkInfo
    """

    result = None
    pulse = pulse_instance()

    if name_or_desc is None:
        name_or_desc = pulse.server_info().default_sink_name

    for s in pulse.sink_list():
        if (s.name == name_or_desc) or (s.description == name_or_desc):
            result = s
            break

    return result


def pulse_source_port(source, name_or_desc):
    """
    Returns the PulseSourceInfo that matches the string, either against the name or the description.

    :param source: the PulseSourceObject to get the port from
    :type source: pulsectl.PulseSourceObject
    :param name_or_desc: the name or description string to look for, uses active one if None
    :type name_or_desc: str
    :return: the PulsePortInfo object or None if not found
    :rtype: pulsectl.pulsectl.PulsePortInfo
    """

    if source is None:
        raise Exception("No source object provided!")

    result = None

    if name_or_desc is None:
        if source.port_active is not None:
            result = source.port_active
    else:
        for port in source.port_list:
            if (port.name == name_or_desc) or (port.description == name_or_desc):
                result = port
                break

    return result


def pulse_sink_port(sink, name_or_desc):
    """
    Returns the PulseSinkInfo that matches the string, either against the name or the description.

    :param sink: the PulseSinkObject to get the port from
    :type sink: pulsectl.PulseSinkObject
    :param name_or_desc: the name or description string to look for, uses active one if None
    :type name_or_desc: str
    :return: the PulseSinkInfo object or None if not found
    :rtype: pulsectl.pulsectl.PulseSinkInfo
    """

    if sink is None:
        raise Exception("No sink object provided!")

    result = None

    if name_or_desc is None:
        if sink.port_active is not None:
            result = sink.port_active
    else:
        for port in sink.port_list:
            if (port.name == name_or_desc) or (port.description == name_or_desc):
                result = port
                break

    return result


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


def pulse_create_profile(source_name=None, sink_name=None, source_port=None, sink_port=None, desc=None):
    """
    Creates and returns a profile.

    :param source_name: the name or description of the pulseaudio source to use, uses current default if None
    :type source_name: str
    :param sink_name: the name or description of the pulseaudio sink to use, uses current default if None
    :type sink_name: str
    :param source_port: the name or description of the source port to use, uses first one of source if None
    :type source_port: str
    :param sink_port: the name or description of the sink port to use, uses first one of sink if None
    :type sink_port: str
    :param desc: the optional description for this profile
    :type desc: str
    """

    source_obj = pulse_source(source_name)
    if source_obj is None:
        if source_name is None:
            raise Exception("No default source available!")
        else:
            raise Exception("Unknown source: %s" % source_name)
    source_port_obj = pulse_source_port(source_obj, source_port)

    sink_obj = pulse_sink(sink_name)
    if sink_obj is None:
        if sink_name is None:
            raise Exception("No default sink available!")
        else:
            raise Exception("Unknown sink: %s" % sink_name)
    sink_port_obj = pulse_sink_port(sink_obj, sink_port)

    result = {}
    result['source'] = {}
    result['source']['device'] = source_obj.name
    if source_port_obj is not None:
        result['source']['port'] = source_port_obj.name
    result['sink'] = {}
    result['sink']['device'] = sink_obj.name
    if sink_port_obj is not None:
        result['sink']['port'] = sink_port_obj.name

    if desc is not None:
        result['description'] = desc

    return result


def pulse_create(config=None, source_name=None, sink_name=None, source_port=None, sink_port=None, desc=None):
    """
    Creates a profile and stores it under the specified file name (or name in config dir) or to stdout if config is None.

    :param config: the file (or name) to store the profile in, output on stdout if None
    :type config: str
    :param source_name: the name or description of the pulseaudio source to use, uses current default if None
    :type source_name: str
    :param sink_name: the name or description of the pulseaudio sink to use, uses current default if None
    :type sink_name: str
    :param source_port: the name or description of the source port to use, uses first one of source if None
    :type source_port: str
    :param sink_port: the name or description of the sink port to use, uses first one of sink if None
    :type sink_port: str
    :param desc: the optional description for this profile
    :type desc: str
    """

    profile = pulse_create_profile(source_name=source_name, sink_name=sink_name,
                                   source_port=source_port, sink_port=sink_port)

    if config is None:
        print(yaml.dump(profile))
    else:
        config_filename = expand_config(config)
        is_config = is_config_name(config)
        if is_config:
            if not init_config_dir():
                raise Exception("Cannot access/create config directory: %s" % config_dir())
        with open(config_filename, 'w') as config_file:
            yaml.dump(profile, config_file)
        if is_config:
            print("Profile written: %s" % config)
        else:
            print("Profile written to: %s" % config_filename)


def pulse_apply_profile(profile):
    """
    Applies the profile dictionary.

    :param profile: the dictionary with source/sink information.
    :type profile: dict
    """

    # sanity checks
    if not "source" in profile:
        raise Exception("No 'source' section in profile!")
    if not "device" in profile['source']:
        raise Exception("No 'device' in 'source' section of profile!")
    if not "sink" in profile:
        raise Exception("No 'sink' section in profile!")
    if not "device" in profile['sink']:
        raise Exception("No 'device' in 'sink' section of profile!")

    # get source
    source = pulse_source(profile['source']['device'])
    if source is None:
        raise Exception("Source device is not available: %s" % profile['source']['device'])
    source_port = None
    if "port" in profile['source']:
        source_port = pulse_source_port(source, profile['source']['port'])
        if source_port is None:
            raise Exception("Source port is not available: %s" % profile['source']['port'])

    # get sink
    sink = pulse_sink(profile['sink']['device'])
    if sink is None:
        raise Exception("Sink device is not available: %s" % profile['sink']['device'])
    sink_port = None
    if "port" in profile['sink']:
        sink_port = pulse_sink_port(sink, profile['sink']['port'])
        if sink_port is None:
            raise Exception("Sink port is not available: %s" % profile['sink']['port'])
        sink.port_active = sink_port

    pulse = pulse_instance()
    pulse.default_set(source)
    if source_port is not None:
        pulse.port_set(source, source_port)
    pulse.default_set(sink)
    if sink_port is not None:
        pulse.port_set(sink, sink_port)


def pulse_apply(config):
    """
    Applies the specified configuration.

    :param config: the configuration name or file
    :type config: str
    """

    config_filename = expand_config(config)
    if not os.path.exists(config_filename):
        if is_config_name(config):
            raise Exception("Profile does not exist: %s (expanded to %s)" % (config, config_filename))
        else:
            raise Exception("Profile file does not exist: %s (expanded to %s)" % (config, config_filename))

    with open(config_filename, "r") as config_file:
        profile = yaml.safe_load(config_file)
        pulse_apply_profile(profile)
