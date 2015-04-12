# Richard Zhao
# script that calculates total time logged

# Total time from all pairs
def displayTime(filename):
    return totalTime(totalTimeList(filename))

# List of elapsed times for each pair
def totalTimeList(filename):
    f = open(filename, 'r')
    lst = scrapeTime(f)
    pairs = pairTimes(lst)
    difference = findDifferences(pairs)
    return difference

# Sums times of all pairs
def totalTime(timeList):
    seconds = 0
    for time in timeList:
        seconds += timeToSeconds(time)
    return secondsToDays(seconds)

# Adds lines that don't begin with '#' '-' or newline
def scrapeTime(f):
    times = []
    for line in f:
        if (line[0] != '#' and line[0] != '-' and line[0] != '\n'):
            times.append(line)
    return times

# Puts adjacent times into tuples
def pairTimes(times):
    pairs = []
    for i in xrange(0, len(times), 2):
        pairs.append((times[i], times[i + 1]))
    return pairs

# Calculates difference in times for one pair
def timeDifference((a, b)):
    start = timeToSeconds(timeFromLine(a))
    end = timeToSeconds(timeFromLine(b))
    difference = end - start
    if (difference < 0):
        difference += 24 * 3600
    return secondsToTime(difference)

# Returns a list of the time differences for each pair
def findDifferences(pairs):
    differences = []
    for (start, end) in pairs:
        differences.append(timeDifference((start, end)))
    return differences

# Finds the time in 'HH:MM:SS' form from a line
def timeFromLine(line):
    compenents = line.split()
    for item in compenents:
        if (len(item) != 8):
            continue
        if (item[0].isdigit() == False):
            continue
        if (item[1].isdigit() == False):
            continue
        if (item[2] != ':'):
            continue
        return item

# Takes a string in form 'HH:MM:SS' and converts to seconds
def timeToSeconds(time):
    hourMinuteSecond = time.split(':')
    hours = int(hourMinuteSecond[0])
    minutes = int(hourMinuteSecond[1])
    seconds = int(hourMinuteSecond[2])
    return 3600 * hours + 60 * minutes + seconds

# Converts seconds to 'HH:MM:SS'
def secondsToTime(seconds):
    hours = seconds / 3600
    hoursRemainder = seconds % 3600
    minutes = hoursRemainder / 60
    minutesRemainder = hoursRemainder % 60
    HH = "%.2d" % hours
    MM = "%.2d" % minutes
    SS = "%.2d" % minutesRemainder
    return HH + ':' + MM + ':' + SS

# Converts seconds to 'DD:HH:MM:SS' format
def secondsToDays(seconds):
    days = seconds / (24 * 3600)
    daysRemainder = seconds % (24 * 3600)
    hours = daysRemainder / 3600
    hoursRemainder = daysRemainder % 3600
    minutes = hoursRemainder / 60
    minutesRemainder = hoursRemainder % 60
    DD = "%.2d" % days
    HH = "%.2d" % hours
    MM = "%.2d" % minutes
    SS = "%.2d" % minutesRemainder
    return DD + ':' + HH + ':' + MM + ':' + SS

print "Total time:", displayTime("timesheet.txt")