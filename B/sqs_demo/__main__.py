import sys
import os
import argparse

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import sqs_demo

my_parser = argparse.ArgumentParser(
    prog='sqs_demo',
    description='Show basic aws sqs usage',
    add_help=True
)

my_parser.add_argument(
    'mode',
    choices=['r', 's'],
    help='operation mode: r for reciever, s for sender'
)
my_parser.add_argument(
    'name',
    type=str,
    help='SQS queue name'
)

args = my_parser.parse_args()
if args.mode == 'r':
    sqs_demo.reciever_loop(args.name)
else:
    sqs_demo.sender_loop(args.name)