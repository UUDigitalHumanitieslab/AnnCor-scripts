#!/usr/bin/env python3
"""
Command line interface for adding morphological information to CHAT files.
"""

import sys
import argparse
import coloredlogs

from conversion import morph_enricher
from conversion import pos_mapping

DEFAULT_MAPPING = "conversion/data/pos_mapping.csv"

def main(argv):
    """
    Main entry point.
    """

    coloredlogs.install()

    try:
        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument(
            "-c", "--chat",
            dest="chat_filename",
            help="The CHAT file to enrich.",
            metavar="FILE",
            required=True)
        parser.add_argument(
            "-p", "--pos",
            dest="pos_filename",
            help="The Treebank LASSY/Alpino XML file containing the POS information.",
            metavar="FILE",
            required=True)
        parser.add_argument(
            "-m", "--mapping",
            dest="mapping_filename",
            help="The mapping file to use.",
            metavar="FILE")

        parser.set_defaults(mapping_filename=DEFAULT_MAPPING)

        options = parser.parse_args(argv)

        perform_map(options.mapping_filename, options.chat_filename, options.pos_filename)
    except Exception as exception:
        sys.stderr.write(repr(exception) + "\n")
        sys.stderr.write("for help use --help\n\n")
        raise exception

def perform_map(mapping_filename, chat_filename, pos_filename):
    """
    Perform the mapping and output to console.
    """

    mapping = pos_mapping.PosMapping()
    mapping.read(mapping_filename)

    enricher = morph_enricher.MorphEnricher(mapping)
    for line in enricher.map(chat_filename, pos_filename):
        print(line)

main(sys.argv[1:])
