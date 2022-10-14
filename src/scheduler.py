import argparse
import sys
import os
import re
import json

from cls.domain import DomainConstructor
from cls.template import BreakTemplateParser

def get_span_json(data_path, span_id):
    with open(data_path) as data_file:
        data_json = json.load(data_file)
    return data_json[span_id]


def is_time_valid(time_string):
    if len(time_string) != len("HH:MM:SS"):
        return False
    
    time_exp = re.compile("[0-2][0-9]:[0-5][0-9]:[0-5][0-9]")
    if time_exp.match(time_string) is None:
        return False
    
    hour = int(time_string[0:2])
    if hour >= 24:
        return False
    
    return True    


def check_args(args):
    if not os.path.isfile(args.data_path):
        raise FileNotFoundError(f"File with path {args.data_path} wasn't found!")
    
    for time_arg in [args.start_time, args.end_time]:
        if not is_time_valid(time_arg):
            raise ValueError(f"argument '{time_arg}' has invalid time format! Valid example is '23:59:59'.")
        
    if args.start_time > args.end_time:
        raise ValueError("Given time range is invalid!")


def parse_args(argv):
    parser = argparse.ArgumentParser(description='Break scheduler for university classes')
    
    required_args = {
        "--start-time": "Start time for classes, in the following format - HH:MM:SS",
        "--end-time": "End time for classes, in the following format - HH:MM:SS",
        "--data-path": "Path to data.json file",
        "--span-id": "Break template id in data.json file"
    }
    
    for flag, info in required_args.items():
        parser.add_argument(flag, help=info, required=True)

    args = parser.parse_args(argv)
    check_args(args)
    return args


def main(args):
    cons = DomainConstructor(get_span_json(args.data_path, args.span_id), args.start_time, args.end_time)
    
    initial_condition = 2 * BreakTemplateParser.HOUR_TO_SECONDS
    result = []
    while not result and initial_condition >= 0:
        result = cons.get(initial_condition)
        initial_condition -= 15 * BreakTemplateParser.MINUTE_TO_SECONDS
    
    print(result)

if __name__ == "__main__":
    main(parse_args(sys.argv[1:]))
