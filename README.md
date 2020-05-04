![CI](https://github.com/pontushojer/MultiQC_BLR/workflows/CI/badge.svg?branch=master)
# MultiQC BLR Plugin

A MultiQC plugin for the [BLR analysis pipeline](https://github.com/FrickTobias/BLR). The plugin is based on [example_plugin](https://github.com/MultiQC/example-plugin). 

### Usage

To use this code, you need to install MultiQC and then your code. For example:

```bash
pip install MultiQC
python setup.py install
```

Use `python setup.py develop` if you're actively working on the code - then you don't need to rerun the installation every time you make an edit _(though you still do if you change anything in `setup.py`)_.

### Disabling the plugin

In this example plugin, I have defined a single additional command line flag - `--disable-blr-plugin`. When specified, it sets a new MultiQC config value to `True`. This is checked in every plugin function; the function then returns early if it's `True`.

In this way, we can effectively disable the plugin code and allow native MultiQC execution. Note that a similar approach could be used to _enable_ a custom plugin or feature.
