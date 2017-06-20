#!/usr/bin/env python3
"""
Handles the mapping of a POS Lassy XML node to the format used in CHAT.
"""

from enum import Enum
import csv
import logging

class WordForm(Enum):
    """
    Different word forms to be used for formatting.
    """

    LEMMA = "lemma"
    ROOT = "root"

class PosMapping:
    """
    Mapping of POS nodes to Lassy XML format. Use read() to initialize the mapping.
    """

    def __init__(self):
        self.lookup = {}

    def __getitem__(self, key):
        return self.lookup[key]

    def read(self, filename):
        """
        Read the mapping file, expecting a semicolon separated file containing 4 columns:
         * Lassy POS tag
         * CHAT POS tag
         * Word form to use
         * Affix (optional)
        """
        self.lookup = {}

        with open(filename) as csv_file:
            for row in csv.reader(csv_file, delimiter=';'):
                if row[3] == "":
                    postfix = None
                else:
                    postfix = row[3]

                self.lookup[row[0]] = (row[1], WordForm(row[2]), postfix)

    def map(self, pos_node):
        """
        Map a POS Lassy node to a morphological tag as used in CHAT.
        """

        mapping = self.lookup.get(pos_node.tag)
        if mapping:
            (pos_tag, word_form_type, affix) = mapping
            if word_form_type == WordForm.LEMMA:
                stem = pos_node.lemma
            elif word_form_type == WordForm.ROOT:
                stem = pos_node.root
            else:
                raise Exception("Unknown word form type: {0}".format(word_form_type))

            if affix is None:
                return "{0}|{1}".format(pos_tag, stem)
            else:
                return "{0}|{1}{2}".format(pos_tag, stem, affix)
        else:
            logging.warning("No mapping exists for POS %s, word: %s", pos_node.tag, pos_node.word)
            return None
