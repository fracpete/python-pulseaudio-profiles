# python-pulse-profiles
Simple command-line tool to create and apply pulseaudio profiles under Linux.

Uses the [pulsectl](https://github.com/mk-fg/python-pulse-control) library
underneath the hood.

## Installation

You can install the tool via `pip`:

```commandline
pip install python-pulseaudio-profiles
```

## Commands

### Info

If you want to output information about your PulseAudion setup, then you
can use `ppp-info`:

```
usage: ppp-info [-h] [--list_sources] [--list_sinks] [--volume] [--verbose]

Outputs PulseAudio information in YAML format

optional arguments:
  -h, --help      show this help message and exit
  --list_sources  whether to list all the available source
  --list_sinks    whether to list all the available sinks
  --volume        whether to include the (average) volume across all channels
  --verbose       whether to be more verbose in the output
```

### Create

For creating a configuration you can use `ppp-create`, either using the current 
defaults or overriding them with specific source/sink.

```
usage: ppp-create [-h] [--config NAME_OR_FILE] [--source NAME_OR_DESC]
                  [--source_port NAME_OR_DESC] [--sink NAME_OR_DESC]
                  [--sink_port NAME_OR_DESC] [--desc DESC] [--volume]

Creates a PulseAudio profile in YAML format.

optional arguments:
  -h, --help            show this help message and exit
  --config NAME_OR_FILE
                        the file to store the profile in, outputs it to stdout
                        if not provided
  --source NAME_OR_DESC
                        the specific pulseaudio source to use (name or
                        description), otherwise current default is used
  --source_port NAME_OR_DESC
                        the specific pulseaudio source port to use (name or
                        description), otherwise currently active one is used
  --sink NAME_OR_DESC   the specific pulseaudio sink to use (name or
                        description), otherwise current default is used
  --sink_port NAME_OR_DESC
                        the specific pulseaudio sink port to use (name or
                        description), otherwise currently active one is used
  --desc DESC           the optional description for this profile
  --volume              whether to include the (average) volume across all
                        channels
``` 

### List

You can list configurations using `ppp-list`:

```
usage: ppp-list [-h] [--verbose]

Lists all the available profiles stored in $HOME/.config/python-pulseaudio-
profiles.

optional arguments:
  -h, --help  show this help message and exit
  --verbose   whether to output the content of the profiles as well
```

### Apply

You can apply a configuration using `ppp-apply`:

```
usage: ppp-apply [-h] --config NAME_OR_FILE [--volume]

Applies a PulseAudio profile in YAML format.

optional arguments:
  -h, --help            show this help message and exit
  --config NAME_OR_FILE
                        the file (or config name) to load the profile from,
                        outputs it to stdout if not provided
  --volume              whether to set the (average) volume across all
                        channels
```

### Delete

You can remove a configuration using `ppp-rm`:

```
usage: ppp-rm [-h] --config NAME

Deletes the specified profile stored in $HOME/.config/python-pulseaudio-
profiles.

optional arguments:
  -h, --help     show this help message and exit
  --config NAME  the config name to delete
```
