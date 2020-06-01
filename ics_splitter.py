"""
A handy script for extracting all events from a particular year
from an ICS file into another ICS file.

@author Derek Ruths (druths@networkdynamics.org)
"""

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('input_file', help='the input ICS file')
parser.add_argument('year', help='the year of dates to extract')
parser.add_argument('output_file', help='the output ICS file')

args = parser.parse_args()

print('Extracting {} events from {} into {}'.format(args.year, args.input_file,
                                                    args.output_file))

created_pattern = re.compile('^DTSTART.+%s' % args.year)

in_fname = args.input_file
out_fname = args.output_file

infh = open(in_fname, 'r')

# parsing constants
BEGIN_CALENDAR = 'BEGIN:VCALENDAR'
END_CALENDAR = 'END:VCALENDAR'
BEGIN_EVENT = 'BEGIN:VEVENT'
END_EVENT = 'END:VEVENT'

CREATED2017_OPENER = 'CREATED:2020'

in_preamble = True
in_event = False
event_content = None
event_in_2017 = False

event_count = 0
out_event_count = 0

with open(out_fname, 'w') as outfh:
    for line in infh:
        if in_preamble and line.startswith(BEGIN_EVENT):
            in_preamble = False

        if in_preamble:
            outfh.write(line)
        else:
            if line.startswith(BEGIN_EVENT):
                event_content = []
                event_count += 1
                event_in_2017 = False
                in_event = True

            if in_event:
                if created_pattern.match(line):
                    event_in_2017 = True
                event_content.append(line)

            if line.startswith(END_EVENT):
                in_event = False

                if event_in_2017:
                    out_event_count += 1
                    outfh.write(''.join(event_content))
    outfh.write(END_CALENDAR)
    outfh.close()

# done!
print('wrote {} of {} events'.format(out_event_count, event_count))
