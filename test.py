#!/usr/bin/env python3


import argparse
# Initialize parser with a short description
parser = argparse.ArgumentParser()

# Add positional and optional arguments
parser.add_argument('input_file', nargs='*', help='file to be compressed')
parser.add_argument('output_file', nargs='?', help='compressed output file')
parser.add_argument('--alg', help='algorithm will be used', default="Empty")
parser.add_argument('-H', '--hard_links', action='store_true', default=True)
# Parse argument
args = parser.parse_args()

# if not vars(args):
#     parser.print_help()
#     parser.exit(1)
print('Input file: {}'.format(args.input_file))
print('Output file: {}'.format(args.output_file))
print('Algorithm: {}'.format(args.alg))
print('Algorithm: {}'.format(args.hard_links))
