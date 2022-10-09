import argparse
import sys
import json

def get_one_break():
    pass


def read_from_json(args):
    with open(args.data_path) as json_file:
        json_data = json.load(json_file)
        span_data = json_data[args.span_id]
        breaks = []
        for template in span_data:
            breaks.append(get_one_break(template))


def convert_time_to_seconds(time):
    HOUR_TO_SECONDS = 3600
    MINUTE_TO_SECONDS = 60
    split_time = time.split()
    return int(split_time[0]) * HOUR_TO_SECONDS + \
        int(split_time[1]) * MINUTE_TO_SECONDS + int(split_time[2])


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
