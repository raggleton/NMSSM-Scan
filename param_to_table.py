#!/usr/bin/env python

"""
Convert JSON params file to latex table

Usage:

To print to screen:
    python param_to_table.py <param JSON>

To print to file:
    python param_to_table.py <param JSON> -o <file.tex>

"""


import argparse
import json
import sys


def texify_key(key):
    replacement_dict = {
        "KAPPA": r"\kappa",
        "AKAPPA": r"A_{\kappa}",
        "LAMBDA": r"\lambda",
        "ALAMBDA": r"A_{\lambda}",
        "MUEFF": r"\mu_{\rm{eff}}",
        "TANB": r"\tan\beta",
    }
    return replacement_dict.get(key, key)


def convert_json_to_tex(param_dict, only_contents):
    """Converts json dict to tex table.

    only_contents : bool
        If True, only prints table contents, not boilerplate code.
    """
    if only_contents:
        tex = ""
    else:
        tex = r"""\begin{table}[]
    \centering
    \begin{tabular}{cc}
"""
    tex += r"""        \hline
        Parameter & Range \\
        \hline
"""
    for key, prange in param_dict.iteritems():
        key_tex = texify_key(key)
        # key_tex = key
        tex += r"""        $%s$ & %g - %g \\""" % (key_tex, prange['min'], prange['max'])
        tex += "\n"
    tex += r"""        \hline"""

    if not only_contents:
        tex += "\n"
        tex += r"""    \end{tabular}
    \caption{}
    \label{tab:}
\end{table}"""
    return tex


def main(in_args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("param", help="JSON params file")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("-c", "--contents", action='store_true',
        help="Only produce table contents, not full table boilerplate")
    args = parser.parse_args(in_args)


    # read in JSON file with parameters and bounds
    with open(args.param) as json_file:
        param_dict = json.load(json_file)
        # remove any comments
        rm_keys = []
        for k in param_dict.iterkeys():
            if k.startswith('_'):
                rm_keys.append(k)
        for k in rm_keys:
            del param_dict[k]

    table_contents = convert_json_to_tex(param_dict, args.contents)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(table_contents)
    else:
        print table_contents


if __name__ == "__main__":
    main()
