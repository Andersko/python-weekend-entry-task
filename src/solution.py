"""Main module from which the tool is run.

Can be run as main script, or imported as a module. If imported as a module, run the tool by calling solution.run(...)
function, with tool arguments. For more info check documentation of mentioned function.
"""
from argparse import ArgumentParser

# internal
import csv_handler
import flights
from exceptions import InvalidCvsFormatError


def run(dataset, orig, dest, bags):
    """Run the tool "solution".

    :param dataset: Tool's positional argument `dataset`.
    :param orig: Tool's positional argument `orig`.
    :param dest: Tool's positional argument `dest`.
    :param bags: Tool's optional argument `bags`.
    """
    print(flights.search(dataset, orig, dest, bags))


if __name__ == '__main__':
    parser = ArgumentParser(description='''tool for finding all possible combinations of flights in provided
                                           data, based on search parameters and printing them sorted by price to
                                           standard output''')
    parser.add_argument('file', help='input CSV data')
    parser.add_argument('orig', metavar='origin', help='airport code of origin')
    parser.add_argument('dest', metavar='destination', help='airport code of destination')
    parser.add_argument('--bags', '-b', default=0, type=int, metavar='number',
                        help='number of requested bags, defaults to zero')
    namespace = parser.parse_args()

    try:
        csv_handler.check_format(namespace.file)
        dataset = csv_handler.to_2d_list(namespace.file)
    except (InvalidCvsFormatError, FileNotFoundError, PermissionError) as e:
        exit(e)

    run(dataset, namespace.orig, namespace.dest, namespace.bags)
