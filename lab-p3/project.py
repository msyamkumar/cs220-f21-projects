from csv import DictReader as __DictReader

# key: (energy_idx, year), val: Energy Consumed by the Electric Power Sector in Trillion Btu)
__data = None

# key: Energy type, val: energy index
__energy_to_idx = None


def init(path):
    """init(path) must be called to load data before other calls will work.  You should call it like this: init("energy.csv")"""

    global __data
    global __energy_to_idx

    if path != 'energy.csv':
        print("WARNING!  Opening a path other than energy.csv.  " +
              "That's fine for testing your code yourself, but energy.csv " +
              "will be the only file around when we test your code " +
              "for grading.")

    __data = {}
    __energy_to_idx = {}

    with open(path) as f:
        reader = __DictReader(f)
        for row in reader:
            energy_idx = int(row['index'])
            __energy_to_idx[row['energy type']] = energy_idx
            for year in range(2015, 2020+1):
                __data[(energy_idx, year)] = float(row[str(year)])

def dump():
    """prints all the data to the screen"""
    if __energy_to_idx == None:
        raise Exception("you did not call init first")
    
    for energy in sorted(__energy_to_idx.keys()):
        energy_idx = __energy_to_idx[energy]
        print("%-7s [Index %d]" % (energy, energy_idx))
        for year in range(2015, 2020+1):
            print("  %d: %f Trillion Btu" % (year, __data[(energy_idx, year)]))
        print()


def get_idx(energy):
    """get_idx(energy) returns the index of the specified energy."""
    if __energy_to_idx == None:
        raise Exception("you did not call init first")
    if not energy in __energy_to_idx:
        raise Exception("No energy '%s', only these: %s" %
                        (str(energy), ','.join(list(__energy_to_idx.keys()))))
    return __energy_to_idx[energy]


def get_consumption(energy_idx, year=2020):
    """get_consumption(energy_idx, year) returns the Btu consumed (in Trillions) in the specified energy in specified year."""
    if __data == None:
        raise Exception("you did not call init first")
    if not (energy_idx, year) in __data:
        raise Exception("No data for energy %s, in year %s" %
                        (str(energy_idx), str(year)))
    return __data[(energy_idx, year)]
