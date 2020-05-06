#!/usr/bin/env python
""" BLR MultiQC plugin module for general stats"""

from __future__ import print_function
from collections import OrderedDict
import logging

from multiqc import config
from multiqc.plots import table
from multiqc.modules.base_module import BaseMultiqcModule

from multiqc_blr.utils import update_sample_name

# Initialise the main MultiQC logger
log = logging.getLogger('multiqc')


class MultiqcModule(BaseMultiqcModule):

    def __init__(self):

        # Halt execution if we've disabled the plugin
        if config.kwargs.get('disable_plugin', True):
            return None

        # Initialise the parent module Class object
        super(MultiqcModule, self).__init__(
            name="HapCUT2",
            target="HapCUT2",
            href="https://github.com/vibansal/HapCUT2",
            anchor="hapcut2",
            info=" is a package for haplotype assembly from sequencing data."
        )

        # Create headers
        self.headers = OrderedDict()
        self.headers['switch rate'] = {
            'title': 'Switch rate',
            'description': 'switch errors as a fraction of possible positions for switch errors',
            'format': '{:,.7f}',
            'placement': 1
            }

        self.headers['mismatch rate'] = {
            'title': 'Mismatch rate',
            'description': 'mismatch errors as a fraction of possible positions for mismatch errors',
            'format': '{:,.7f}',
            'placement': 2
        }

        self.headers['flat rate'] = {
            'title': 'Flat rate',
            'description': 'flat errors as a fraction of possible positions for flat errors',
            'format': '{:,.7f}',
            'hidden': True,
        }

        self.headers['phased count'] = {
            'title': 'Phased count',
            'description': 'count of total SNVs phased in the test haplotype',
            'format': '{:,.0f}',
            'placement': 3
        }

        self.headers['AN50'] = {
            'title': 'AN50 (Mbp)',
            'description': 'the AN50 metric of haplotype completeness',
            'format': '{:,.3f}',
            'hidden': True
        }

        self.headers['N50'] = {
            'title': 'N50 (Mbp)',
            'description': 'the N50 metric of haplotype completeness',
            'format': '{:,.3f}',
            'placement': 4
        }

        self.headers['num snps max blk'] = {
            'title': 'SNPs in max blk',
            'description': 'the fraction of SNVs in the largest (most variants phased) block',
            'format': '{:,.0f}',
            'placement': 5
        }

        # Find and load any input files for this module
        self.phasing_data = dict()
        for f in self.find_log_files('hapcut2/phasing_stats', filehandles=True):
            sample_name = update_sample_name(f["s_name"])
            self.phasing_data[sample_name] = dict()
            
            for parameter, value in self.parse_phasing_stats(f["f"]):
                self.phasing_data[sample_name][parameter] = value

        # Nothing found - raise a UserWarning to tell MultiQC
        if len(self.phasing_data) == 0:
            log.debug("Could not find any reports in {}".format(config.analysis_dir))
            raise UserWarning

        log.info("Found {} reports".format(len(self.phasing_data)))

        # Write parsed report data to a file
        self.write_data_file(self.phasing_data, f"hapcut2_phasing_stats")

        pconfig = {
            'id': 'hapcut2_phasing_stats_table',
            'title': "HapCUT2 phasing stats",
        }
        table_html = table.plot(self.phasing_data, self.headers, pconfig)

        # Add a report section with table
        self.add_section(
            name="HapCUT2 phasing stats",
            description=f"Statistics table",
            helptext='''
            Description of statistics (taken from https://github.com/vibansal/HapCUT2/tree/master/utilities):
            ''',
            plot=table_html
        )

    @staticmethod
    def parse_phasing_stats(file):
        """
        This generator yields key-value pairs for the data from the line following `---` until the next line
        staring with `===`.
        """
        for line in file:
            # Collect parameter and value
            parameter, value = line.strip().split(":", maxsplit=1)
            value = float(value.strip())

            # Make N50 and AN50 stats per Mbp instead of bp.
            if parameter in ["N50", "AN50"]:
                value /= 1_000_000

            yield parameter, value
