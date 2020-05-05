#!/usr/bin/env python
""" BLR MultiQC plugin module for general stats"""

from __future__ import print_function
from collections import OrderedDict
import logging

from multiqc import config
from multiqc.plots import table
from multiqc.modules.base_module import BaseMultiqcModule


# Initialise the main MultiQC logger
log = logging.getLogger('multiqc')


class MultiqcModule(BaseMultiqcModule):

    def __init__(self):

        # Halt execution if we've disabled the plugin
        if config.kwargs.get('disable_plugin', True):
            return None

        # Initialise the parent module Class object
        super(MultiqcModule, self).__init__(
            name="Stats",
            target="stats",
            anchor="stats",
            info=" is collection of statistics from the different BLR commandline tools."
        )

        # Find and load any input files for this module
        self.headers = dict()
        self.stats_data = dict()
        for f in self.find_log_files('stats', filehandles=True):
            tool_name = self.get_tool_name(f["f"])
            if tool_name not in self.stats_data:
                self.stats_data[tool_name] = dict()
                self.headers[tool_name] = OrderedDict()

            self.stats_data[tool_name][f["s_name"]] = dict()
            for parameter, value in self.parse(f["f"]):
                header_name = parameter.lower().replace(" ", "_")
                self.stats_data[tool_name][f["s_name"]][header_name] = value

                self.headers[tool_name][header_name] = {
                    'title': parameter
                }

        # Nothing found - raise a UserWarning to tell MultiQC
        if len(self.stats_data) == 0:
            log.debug("Could not find any reports in {}".format(config.analysis_dir))
            raise UserWarning

        log.info("Found {} reports".format(len(self.stats_data)))

        # For each tool generat a separat statistics table for all found samples.
        for tool_name, data in self.stats_data.items():
            tool_name_title = tool_name.capitalize()

            # Write parsed report data to a file
            self.write_data_file(data, f"{tool_name}_stats")

            pconfig = {
                'id': 'blr_stats_table',
                'title': f"{tool_name_title} stats",
            }
            table_html = table.plot(data, self.headers[tool_name], pconfig)

            # Add a report section with table
            self.add_section(
                name=tool_name_title,
                description=f"Statistics table for data from BLR tool {tool_name}",
                helptext='''
                This longer description explains what exactly the numbers mean
                and supports markdown formatting. This means that we can do _this_:

                * Something important
                * Something else important
                * Best of all - some `code`

                Doesn't matter if this is copied from documentation - makes it
                easier for people to find quickly.
                ''',
                plot=table_html
            )

    @staticmethod
    def get_tool_name(file):
        """ Get the tools name by locating the line starting with 'STATS SUMMARY' which contains the tool name in the
         format e.g 'STATS SUMMARY - blr.cli.tool_name. Return tool name"""
        for line in file:
            if line.startswith("STATS SUMMARY"):
                return line.strip().split(".")[-1]

        return None

    @staticmethod
    def parse(file):
        """
        This generator yields key-value pairs for the data from the line following `---` until the next line
        staring with `===`.
        """
        collect = False
        for line in file:
            # Collect stats after first line starting with '---' and stop when starts with '==='
            if line.startswith("---"):
                collect = True
                continue
            elif line.startswith("===") and collect:
                break

            if collect:
                # Collect parameter and value
                parameter, value = list(filter(None, line.strip().split("  ")))
                value = value.strip().replace(",", "")

                yield parameter, float(value)
