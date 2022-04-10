"""Module for handling csv format input.
"""
import csv
from datetime import datetime

# internal
from exceptions import InvalidCvsFormatError
from constants import *


def check_format(csvfile):
    """Check format of csv file in terms of program input specification.

    :param csvfile: Absolute or relative path from file, from which the tool was run.
    :type csvfile: str
    :raise InvalidCvsFormatError: If file is not formatted according to specification.
    """
    with open(csvfile, newline='') as f:
        reader = csv.reader(f)

        try:
            headers = next(reader)
        except StopIteration:
            raise InvalidCvsFormatError(f'{csvfile}: empty file')

        if headers != CSV_HEADERS:
            raise InvalidCvsFormatError('Invalid or missing headers.')

        for row in reader:
            if len(row) != 8:
                raise InvalidCvsFormatError(f'Invalid number of records at row {reader.line_num}')
            try:
                datetime.strptime(row[DEPARTURE], '%Y-%m-%dT%H:%M:%S')
                datetime.strptime(row[ARRIVAL], '%Y-%m-%dT%H:%M:%S')
            except ValueError:
                raise InvalidCvsFormatError(f'Incorrect date format at row {reader.line_num}')
            try:
                if float(row[BASE_PRICE]) < 0 or float(row[BAG_PRICE]) < 0 or int(row[BAGS_ALLOWED]) < 0:
                    raise InvalidCvsFormatError(f'Row {reader.line_num}: base and bag price and bags allowed must be'
                                                f'zero or more')
            except ValueError:
                raise InvalidCvsFormatError(f'Invalid base price or bag price or bags allowed value at line'
                                            f' {reader.line_num}')

        if reader.line_num == 1:
            raise InvalidCvsFormatError('No data in CVS file.')


def to_2d_list(csvfile):
    """Transform csvfile data into 2D list.

    :param csvfile: Absolute or relative path from file, from which the tool was run.
    :type csvfile: str
    :return: list of lists of str: 2-dimensional list.
    """
    with open(csvfile, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        return list(reader)
