import argparse
import sys
import os
import re
import json
from dataclasses import dataclass
from itertools import product


@dataclass
class BreakInterval:
    begin_sec: int
    end_sec: int


class BreakTemplateParser:
    HOUR_TO_SECONDS = 3600
    MINUTE_TO_SECONDS = 60
    
    @staticmethod
    def is_valid_interval(interval, class_start_in_seconds, class_end_in_seconds):
        return interval.begin_sec > class_start_in_seconds and interval.end_sec < class_end_in_seconds
    
    @classmethod
    def convert_time_to_seconds(cls, time):
        split_time = time.split(':')
        return int(split_time[0]) * cls.HOUR_TO_SECONDS + \
        int(split_time[1]) * cls.MINUTE_TO_SECONDS + int(split_time[2])
    
    def __init__(self, template_json, class_begin_time, class_end_time):
        self.class_start_in_seconds = self.convert_time_to_seconds(class_begin_time)
        self.class_end_in_seconds = self.convert_time_to_seconds(class_end_time)
        self.is_relative_to_start = True if template_json["start_time_type"] == "RELATIVE_TO_CLASS_START" else False
        self.start_times = template_json["start_times"]
        self.duration = template_json["break_duration"]

    def construct_valid_interval_list(self):
        intervals = []
        for break_start_time in self.start_times:
            break_start_in_seconds = self.convert_time_to_seconds(break_start_time)
            if self.is_relative_to_start:
                interval = BreakInterval(self.class_start_in_seconds + break_start_in_seconds,
                                         self.class_start_in_seconds + break_start_in_seconds + self.duration)
            else:
                interval = BreakInterval(self.class_end_in_seconds - break_start_in_seconds,
                                         self.class_end_in_seconds - break_start_in_seconds + self.duration)
            if self.is_valid_interval(interval, self.class_start_in_seconds, self.class_end_in_seconds):
                intervals.append(interval)
        return intervals


class Domain:
    def __init__(self, span_json, class_begin_time, class_end_time):
        self.templates = []
        for template_json in span_json:
            parser = BreakTemplateParser(template_json, class_begin_time, class_end_time)
            self.templates.append(parser.construct_valid_interval_list())

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
    domain = Domain(get_span_json(args.data_path, args.span_id), args.start_time, args.end_time)
    """
    initial_condition = 2 * Domain.HOUR_TO_SECONDS
    result = []
    while not result and initial_condition >= 0:
        result = Domain.get(initial_condition)
        initial_condition -= 15 * Domain.MINUTE_TO_SECONDS
    
    print(result)
    """

if __name__ == "__main__":
    main(parse_args(sys.argv[1:]))
