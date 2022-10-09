import argparse
import sys


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description='Break scheduler for university classes')
    parser.add_argument('--start-time',
                        help='Start time for classes',
                        required=True)
    parser.add_argument('--end-time',
                        help='End time for classes',
                        required=True)
    parser.add_argument('--data-path',
                        help='Path to data.json file',
                        required=True)
    parser.add_argument('--span-id',
                        help='Break template id in data.json file',
                        required=True)

    return parser.parse_args(argv)


def main(args):
    print(args.start_time)


if __name__ == '__main__':
    main(parse_args(sys.argv[1:]))
