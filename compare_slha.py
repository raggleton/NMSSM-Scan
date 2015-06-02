"""
Takes a given BLOCK from any number of SLHA files and compares them.

Handy for cross-checking files.
"""


import sys
import argparse
from pprint import pprint
import numpy as np
import pandas as pd


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 150)


def get_blocks(filenames, block_name):
    """Get block from files. Returns dict of filename:contents"""
    blocks = {}  # dict of filename: contents
    for f_name in filenames:
        with open(f_name, 'r') as f:
            contents = []  # store lines as list
            store = False  # flag whether to store line from file
            for line in f:
                if line.strip().startswith('#'):
                    continue
                # find where blocks start/stop
                if "BLOCK" in line:
                    if block_name in line:
                        store = True
                        continue
                    else:
                        store = False
                        # skip rest of file if we have what we need
                        if contents:
                            break
                if store:
                    contents.append(line.strip())

            blocks[f_name] = contents

    return blocks

def make_dataframe(block_name, blocks):
    """
    Make DataFrame from blocks, each columns is a different field,
    each row is for a different file.
    """
    names = {} # store names corresponding to column ids
    all_rows = [] # store list of dicts of column_id: value
    for k, v in blocks.iteritems():
        # to hold table info for this file
        info = {}
        for line in v:
            # split around the #. parts[0] is the contents, parts[1] is the column header
            # (but note programs use diff conventions...)
            parts = [p.strip() for p in line.split('#')]
            data, comment = parts

            # for most blocks, we use the first part of parts[0] to ID what the row means
            # BUT this doens't work for all e.g. DCINFO
            id_not_first_blocks = ["DCINFO"]
            if block_name in id_not_first_blocks:
                pass
            else:
                col_id, contents = data.split()
                names[col_id] = comment
                info[col_id] = contents
        all_rows.append(info)
    # make a DataFrame for this block
    df = pd.DataFrame(all_rows, index=blocks.keys())
    # convert column IDs to string names
    df.rename(columns=names, inplace=True)
    df.reindex_axis(sorted(df.columns), axis=1)
    print df
    return df


def main(in_args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blocks", nargs='+', help="BLOCK names to compare")
    parser.add_argument("--inputs", nargs='+', help="Input SLHA files")
    args = parser.parse_args(args=in_args)

    for block in args.blocks:
        print "BLOCK", block
        blocks = get_blocks(args.inputs, block)
        # pprint(blocks)
        make_dataframe(block, blocks)


if __name__ == "__main__":
    main()

