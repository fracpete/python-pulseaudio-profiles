import os
import pulsectl
import yaml
from pypulseprofiles.config import *


def pulse_instance():
    """
    Returns an Pulse instance.

    :return: the instance
    :rtype: pulsectl.Pulse
    """
    return pulsectl.Pulse(APPLICATION_NAME)


def pulse_source_info(source, volume=False, verbose=False):
    """
    Generates a dictionary from the PulseSourceInfo object.

    :param source: the PulseSourceInfo object to use
    :type source: pulsectl.PulseSourceInfo
    :param volume: whether to include the (average) volume across all channels
    :type volume: bool
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
        if volume:
            result['device']['volume'] = source.volume.value_flat
        if source.port_active is not None:
            result['port'] = {}
            result['port']['name'] = source.port_active.name
            result['port']['description'] = source.port_active.description
    else:
        result['device'] = source.description
        if source.port_active is not None:
            result['port'] = source.port_active.description
        if volume:
            result['volume'] = source.volume.value_flat

    return result


def pulse_sink_info(sink, volume=False, verbose=False):
    """
    Generates a dictionary from the PulseSinkInfo object.

    :param sink: the PulseSinkInfo object to use
    :type sink: pulsectl.PulseSinkInfo
    :param volume: whether to include the (average) volume across all channels
    :type volume: bool
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
        if volume:
            result['device']['volume'] = sink.volume.value_flat
        if sink.port_active is not None:
            result['port'] = {}
            result['port']['name'] = sink.port_active.name
            result['port']['description'] = sink.port_active.description
    else:
        result['device'] = sink.description
        if sink.port_active is not None:
            result['port'] = sink.port_active.description
        if volume:
            result['volume'] = sink.volume.value_flat

    return result


def pulse_info(list_sources=False, list_sinks=False, volume=False, verbose=False):
    """
    Returns a dictionary with information about the setup.

    :param list_sources: whether to list sources
    :type list_sources: bool
    :param list_sinks: whether to list sinks
    :type list_sinks: bool
    :param volume: whether to include the (average) volume across all channels
    :type volume: bool
    :param verbose: whether to be verbose
    :type verbose: bool
    """

    pulse = pulse_instance()

    info = dict()
    info['default_source'] = pulse_source_info(pulse_source(), volume=volume, verbose=verbose)
    info['default_sink'] = pulse_sink_info(pulse_sink(), volume=volume, verbose=verbose)

    if list_sources:
        sources = []
        for s in pulse.source_list():
            sources.append(pulse_source_info(s, volume=volume, verbose=verbose))
        info['sources'] = sources

    if list_sinks:
        sinks = []
        for s in pulse.source_list():
            sinks.append(pulse_sink_info(s, volume=volume, verbose=verbose))
        info['sinks'] = sinks

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


def pulse_create_profile(source_name=None, sink_name=None, source_port=None, sink_port=None, desc=None, volume=False):
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
    :param volume: whether to include the (average) volume across all channels
    :type volume: bool
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
    if volume:
        result['source']['volume'] = source_obj.volume.value_flat
    if source_port_obj is not None:
        result['source']['port'] = source_port_obj.name
    result['sink'] = {}
    result['sink']['device'] = sink_obj.name
    if volume:
        result['sink']['volume'] = sink_obj.volume.value_flat
    if sink_port_obj is not None:
        result['sink']['port'] = sink_port_obj.name

    if desc is not None:
        result['description'] = desc

    return result


def pulse_create(config=None, source_name=None, sink_name=None, source_port=None, sink_port=None, desc=None, volume=False):
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
    :param volume: whether to include the (average) volume across all channels
    :type volume: bool
    """

    profile = pulse_create_profile(source_name=source_name, sink_name=sink_name,
                                   source_port=source_port, sink_port=sink_port,
                                   desc=desc, volume=volume)

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


def pulse_load(config):
    """
    Loads the specified configuration and returns the profile.

    :param config: the configuration name or file
    :type config: str
    :return: the profile
    :rtype: dictionary
    """

    config_filename = expand_config(config)
    if not os.path.exists(config_filename):
        if is_config_name(config):
            raise Exception("Profile does not exist: %s (expanded to %s)" % (config, config_filename))
        else:
            raise Exception("Profile file does not exist: %s (expanded to %s)" % (config, config_filename))

    with open(config_filename, "r") as config_file:
        profile = yaml.safe_load(config_file)
        return profile


def pulse_apply_profile(profile, volume=False):
    """
    Applies the profile dictionary.

    :param profile: the dictionary with source/sink information.
    :type profile: dict
    :param volume: whether to set the volume across all channels (if present)
    :type volume: bool
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
    source_volume = None
    if "volume" in profile['source']:
        source_volume = float(profile['source']['volume'])
    source_port = None
    if "port" in profile['source']:
        source_port = pulse_source_port(source, profile['source']['port'])
        if source_port is None:
            raise Exception("Source port is not available: %s" % profile['source']['port'])

    # get sink
    sink = pulse_sink(profile['sink']['device'])
    if sink is None:
        raise Exception("Sink device is not available: %s" % profile['sink']['device'])
    sink_volume = None
    if "volume" in profile['sink']:
        sink_volume = float(profile['sink']['volume'])
    sink_port = None
    if "port" in profile['sink']:
        sink_port = pulse_sink_port(sink, profile['sink']['port'])
        if sink_port is None:
            raise Exception("Sink port is not available: %s" % profile['sink']['port'])
        sink.port_active = sink_port

    pulse = pulse_instance()
    pulse.default_set(source)
    if volume and source_volume is not None:
        source.volume.value_flat = source_volume
        pulse.volume_set(source, source.volume)
    if source_port is not None:
        pulse.port_set(source, source_port)
    pulse.default_set(sink)
    if volume and sink_volume is not None:
        sink.volume.value_flat = sink_volume
        pulse.volume_set(sink, sink.volume)
    if sink_port is not None:
        pulse.port_set(sink, sink_port)


def pulse_apply(config, volume=False):
    """
    Applies the specified configuration.

    :param config: the configuration name or file
    :type config: str
    :param volume: whether to set the volume across all channels (if present)
    :type volume: bool
    """

    pulse_apply_profile(pulse_load(config), volume=volume)


def pulse_list(verbose=False):
    """
    Lists all the available profiles in the config dir.

    :param verbose: if True the content of the profiles is output as well
    :rtype: bool
    """

    profiles = list_configs()
    if len(profiles) == 0:
        print("No profiles available")
    else:
        print("Available profile(s):")
        for profile in profiles:
            print("-", profile)
            if verbose:
                content = pulse_load(profile)
                lines = yaml.dump(content).split("\n")
                for i in range(len(lines)):
                    lines[i] = "  " + lines[i]
                print("\n".join(lines) + "\n")


def pulse_delete(config):
    """
    Deletes the specified configuration.

    :param config: the configuration name
    :type config: str
    """

    delete_config(config)
    print("Deleted profile: %s" % config)
