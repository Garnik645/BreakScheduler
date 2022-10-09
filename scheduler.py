import argparse
import sys
import os
import json


class BreakTemplate:
    HOUR_TO_SECONDS = 3600
    MINUTE_TO_SECONDS = 60
    
    @staticmethod
    def is_valid_interval(interval, class_start_in_seconds, class_end_in_seconds):
        return interval[0] > class_start_in_seconds and interval[1] < class_end_in_seconds
    
    @classmethod
    def convert_time_to_seconds(cls, time):
        split_time = time.split(':')
        return int(split_time[0]) * cls.HOUR_TO_SECONDS + \
        int(split_time[1]) * cls.MINUTE_TO_SECONDS + int(split_time[2])
    
    def __init__(self, json_template):
        self.start_times = []
        self.duration = int(json_template['break_duration']) * self.MINUTE_TO_SECONDS
        self.is_relative_to_start = True if json_template['start_time_type'] == 'RELATIVE_TO_CLASS_START' else False
        for start_time in json_template['start_times']:
            self.start_times.append(self.convert_time_to_seconds(start_time))
            
    def get_break_intervals(self, class_start, class_end):
        intervals = []
        class_start_in_seconds = self.convert_time_to_seconds(class_start)
        class_end_in_seconds = self.convert_time_to_seconds(class_end)
        for break_start in self.start_times:
            if self.is_relative_to_start:
                interval = (class_start_in_seconds + break_start, class_start_in_seconds + break_start + self.duration)
            else:
                interval = (class_end_in_seconds - break_start, class_end_in_seconds - break_start + self.duration)
            
            if self.is_valid_interval(interval, class_start_in_seconds, class_end_in_seconds):
                intervals.append(interval)
        return intervals
                


class Domain:
    def __init__(self, args):
        self.args = args
        self.break_intervals = []
    
    def collect_template_intervals(self):
        with open(self.args.data_path) as data_file:
            data_json = json.load(data_file)
            span_json = data_json[self.args.span_id]
            for template_json in span_json:
                template_obj = BreakTemplate(template_json)
                intervals = template_obj.get_break_intervals(self.args.start_time, self.args.end_time)
                self.break_intervals.append(intervals)


# todo check time format
def check_args(args):
    if not os.path.isfile(args.data_path):
        raise FileNotFoundError("File with path {} wasn't found!".format(args.data_path))


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description='Break scheduler for university classes')
    
    required_args = {
        '--start-time': 'Start time for classes, in this format - HH:MM:SS',
        '--end-time': 'End time for classes, in this format - HH:MM:SS',
        '--data-path': 'Path to data.json file',
        '--span-id': 'Break template id in data.json file'
    }
    
    for flag, info in required_args.items():
        parser.add_argument(flag, help=info, required=True)

    args = parser.parse_args(argv)
    check_args(args)
    return args


def main(args):
    domain = Domain(args)
    domain.collect_template_intervals()
    print(domain.break_intervals)


if __name__ == '__main__':
    main(parse_args(sys.argv[1:]))
