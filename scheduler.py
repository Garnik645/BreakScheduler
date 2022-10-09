import argparse
import sys
import json


class Break:
    HOUR_TO_SECONDS = 3600
    MINUTE_TO_SECONDS = 60
    
    @classmethod
    def convert_time_to_seconds(cls, time):
        split_time = time.split()
        return int(split_time[0]) * cls.HOUR_TO_SECONDS + \
        int(split_time[1]) * cls.MINUTE_TO_SECONDS + int(split_time[2])
    
    def __init__(self, json_template):
        self.start_times = []
        self.duration = int(json_template['break_duration']) * self.MINUTE_TO_SECONDS
        self.is_relative_to_start = True if json_template['start_time_type'] == 'RELATIVE_TO_CLASS_START' else False
        for start_time in json_template['start_times']:
            self.start_times.append(self.convert_time_to_seconds(start_time))


def read_from_json(args):
    with open(args.data_path) as json_file:
        json_data = json.load(json_file)
        span_data = json_data[args.span_id]
        breaks = []
        for template in span_data:
            breaks.append(Break(template))


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description='Break scheduler for university classes')
    
    required_args = {
        '--start-time': 'Start time for classes',
        '--end-time': 'End time for classes',
        '--data-path': 'Path to data.json file',
        '--span-id': 'Break template id in data.json file'
    }
    
    for flag, info in required_args.items():
        parser.add_argument(flag, help=info, required=True)

    return parser.parse_args(argv)


def main(args):
    print(args.start_time)


if __name__ == '__main__':
    main(parse_args(sys.argv[1:]))
