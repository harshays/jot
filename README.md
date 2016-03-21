### Jot
CLI to quickly add ideas or log events to csv files.

#### Few use cases
* Side project ideas
* Food journal
* Weight tracker

#### Using Jot
```sh
jot -a food "sandwich"
jot -a projects "Jot CLI"
jot -a weight "XX lb"
jot -a {{file}} "{{content}}"
jot --config
jot --help
```

#### Config and custom file properties
Jot uses a JSON config file. Files can be configured to prepend timestamps, counters and/or username whenever they're updated.

1. Files properties are inherited from ```JotFiles['default']```
2. Files that exist but are not explicitly set in the config file use the default config
3. See ```config.json```

#### Setup
1. Install blessings (```pip install blessings```)
2. Set a bash alias to run the script (```alias jot='python /path/to/jot.py'```)
3. Modify ```config.json```
