import argparse

from .console_calendar import main_parser


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='Make ics file', action='store_true')
    parser.add_argument('-d', help='Write diary', action='store_true')
    parser.add_argument('-g', help='Google calendar link', action='store_true')
    parser.add_argument('--no-push', help="Don't push my calendar",
                        action='store_false')
    parser.add_argument('-q', help='Push quickAdd calendar', action='store_true')
    parser.add_argument('-l', help='Calendar lists', action='store_true')

    args = parser.parse_args(args)

    main_parser(vars(args))
