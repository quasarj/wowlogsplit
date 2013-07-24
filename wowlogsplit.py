import csv
import time
import os
from datetime import datetime

from catagorize import catagorize

INFILE="WoWCombatLog.txt"
OUTFILE="test_out.txt"

def get_affliation(srcflags):
    if srcflags & 0x0001 != 0:
        return "Self"
    elif srcflags & 0x0002 != 0:
        return "Party"
    elif srcflags & 0x0004 != 0:
        return "Raid"
    else:
        return "Other"

def write_report(days):
    with open("log_report.txt", 'wb') as out:
        out.write("Days in this log file: {}\n\n".format(len(days)))
        for day in days:
            filename = "log_{}.txt".format(
                datetime.strptime(day['date'], '%M/%d').strftime('%M_%d'))
            guild = catagorize(day['actors'])

            new_filename = "{}__{}".format(guild.lower().replace(' ', '_'), filename)
            print "Renaming {} -> {}".format(filename, new_filename)
            try:
                os.rename(filename, new_filename)
            except:
                print "Something went wrong with that rename :("

            out.write(new_filename + ':\n')
            out.write("I think this is: {}\n".format(guild))
            for actor in day['actors']:
                out.write("\t{}\n".format(actor))

            out.write("\n\n")

days = []

actors_in_this_file = set()

start_time = time.time()

last_date = None
o = None
writer = None
with open(INFILE, 'rb') as f:
    reader = csv.reader(f)
    for i,row in enumerate(reader):
        timestamp, event = row[0].split('  ')
        date, time_ = timestamp.split(' ')
        if date != last_date:
            print "Found a new date: ", date

            # close the exsiting file if there is one
            if o is not None:
                o.close()

            # setup the new output file and writer
            filename = "log_{}.txt".format(
                datetime.strptime(date, '%M/%d').strftime('%M_%d'))
            o = open(filename, 'wb')
            writer = csv.writer(o)

            if last_date is not None:
                days.append({'date': last_date,
                             'actors': actors_in_this_file })
                actors_in_this_file = set()

            last_date = date


        actor = row[2]
        srcflags = int(row[3], 16)

        # is it a player?
        if srcflags & 0x0400 != 0:
            actors_in_this_file.add(actor)
        
        writer.writerow(row)

    # add the last one too
    days.append({'date': date,
                 'actors': actors_in_this_file })

    if o is not None:
        o.close()

write_report(days)

print "Records in source file: {}".format(i)
print "Seconds elapsed: {}".format(time.time() - start_time)
