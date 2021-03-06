#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import arghelper
from arghelper import inputfile
from arghelper import inputdir
from arghelper import check_range
import os
import sys
from functions import *


class SeevisParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("> error: %s\n" % message)
        self.print_help()
        sys.exit(2)


def main(argv=None):
    '''
    Handles the parsing of arguments
    '''
    parser = SeevisParser(
        prog="SEEVIS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""----------------------------------------------
SEEVIS - (S)egmentation-Fr(EE)(VIS)ualisation
----------------------------------------------
Hattab et al. Under the MIT License. """,
        epilog="""
Usage examples:
./seevis.py -i img_directory/
./seevis.py -f filename.csv -s 2
            """)

    # Arguments to be handled
    parser.add_argument("-v", "--version", action="version", version="%(prog)s"
                        "1.0\n")

    parser.add_argument("-i", "--input", default=None, metavar="dir", help="run "
                        "SeeVIS on the supplied "
                        "directory", type=lambda x: arghelper.inputdir(parser, x))

    parser.add_argument("-f", "--file", default=None, help="run "
                        "the Visualisation of SeeVIS", type=inputfile)

    parser.add_argument("-s", help="run colour scheme"
                        "ranging from 1 to 3 "
                        "(default is 1)", nargs="?", default=1, type=check_range)

    try:
        args = parser.parse_args()
        if args.file is None and args.input is None:
            parser.error("--input or --file must be supplied")

        elif args.file is not None and args.input is not None:
            parser.error("please choose either an input dir. or a csv file")

        elif args.file is not None:
            print(parser.description, "\n")
            print("Input file", args.file)
            print("Chosen scheme", args.s)
            st = time.time()
            d = load_data(args.file)
            elapsed_time(st)
            visualise(d, args.s)
            elapsed_time(st)
            print("Press Enter to exit")
            input()

        elif args.input is not None:
            if not args.input.endswith("/"):
                parser.error("please supply a suitable directory (Usage examples below).")
            else:
                print(parser.description, "\n")
                print("Input directory", args.input)
                print("Chosen scheme", args.s)
                st = time.time()
                outdir = preprocess(args.input)
                elapsed_time(st)
                d = get_data(outdir)
                elapsed_time(st)
                visualise(d, args.s)
                elapsed_time(st)
                print("Press Enter to exit")
                input()

    except IOError as msg:
        parser.error(str(msg))

    except KeyboardInterrupt:
        parser.exit(1, "\nExecution aborted")


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    main(sys.argv[1:])
