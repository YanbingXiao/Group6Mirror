import json
import sys
from datetime import datetime

# The current date
today: str = (str)(datetime.now().date())

# Command-line arguments
cliArgs: list[int] = sys.argv[1:]


def storeTime(time) -> None:
    """ Store user-input time into daily statistics, then recalculate the
    historic averages for brushing data.

    Args:
        time: duration of brush session
    """

    # Read the data file
    print("Loading existing data...", end="")
    brushData: dict = json.load(open("toothbrush_daily.json", "r"))
    if not brushData:
        print("Failed to load data!")
        return
    print("Success!")

    # Check for existing daily data
    if today in brushData.keys():
        print(f"Updating entry for date: {today}")
        brushData[today]['brush_count'] += 1
        brushData[today]['brush_time_minutes'].append((float)(time))
    else:
        print(f"Creating new entry for date: {today}")
        brushData[today] = {
            'brush_count': 1,
            'brush_time_minutes': [time]
        }

    # Calculate new historic values
    time_historic: int = 0
    count_historic: int = 0
    total_days: int = len(brushData)
    for day in brushData:
        count_historic += brushData[day]['brush_count']
        for brushTime in brushData[day]['brush_time_minutes']:
            time_historic += brushTime/brushData[day]['brush_count']

    # Write historic values to our data
    averageBrushData: dict = json.load(open("toothbrush_average.json", "r"))
    if not averageBrushData:
        print("Failed to load average data!")
        return
    averageBrushData['historic_brush_time_minutes'] = time_historic/total_days
    averageBrushData['historic_brush_count'] = count_historic/total_days

    # Write changes back to the data file
    print("Writing changes...", end="")
    json.dump(brushData, open("toothbrush_daily.json", "w"), indent=4)
    json.dump(averageBrushData, open("toothbrush_average.json", "w"), indent=4)
    print("Success!")


def showData() -> None:
    """ Print formatted statistics for the daily brush data.
    If no data is found, alert the user.
    """
    # Read the data file
    brushData: dict = json.load(open("toothbrush_daily.json", "r"))
    averageBrushData: dict = json.load(open("toothbrush_average.json", "r"))
    if not brushData or not averageBrushData:
        print("Failed to load data!")
        return
    # Check for existing daily data
    if today in brushData.keys():
        count: int = brushData[today]['brush_count']
        timeSum: float = 0
        for time in brushData[today]['brush_time_minutes']:
            timeSum += time;
           
        timeSum_sec = (int)(timeSum*60)
        timeSum_min, timeSum_sec = divmod(timeSum_sec, 60)
        timeSum_format = '{:02d}:{:02d}'.format(timeSum_min, timeSum_sec)

        histCnt: int = averageBrushData['historic_brush_count']
        histTime: int = averageBrushData['historic_brush_time_minutes']
        
        histTime_sec = (int)(histTime*60)
        histTime_min, histTime_sec = divmod(histTime_sec, 60)
        histTime_format = '{:02d}:{:02d}'.format(histTime_min, histTime_sec)
        print(f"\nBrushing Stats for {today}\n")
        print(f"You brushed {count} time(s) today, for a total of {timeSum_format} minutes!")
        print("\nHere's your daily breakdown:")
        for i in range(len(brushData[today]['brush_time_minutes'])): 
            timeSum_sec = (int)(brushData[today]['brush_time_minutes'][i] * 60)
            timeSum_min, timeSum_sec = divmod(timeSum_sec, 60)
            timeSum_format = '{:02d}:{:02d}'.format(timeSum_min, timeSum_sec)
            print(f"\tBrush {i+1} -> {timeSum_format}")
        print(f"\nOn average, you brush {histCnt} times a day for {histTime_format} minutes per brush\n")
    else:
        print(f"\nNo brush data for {today}\n")


def main():
    """ Handle Command-Line arguments and run appropriate functions """
    if (len(cliArgs) == 0):
        print("*** No command specified, run -h for information ***")
        return
    elif cliArgs[0] == "--store" and len(cliArgs) > 1:
        storeTime((float)(cliArgs[1]))
    elif cliArgs[0] == "--show":
        showData()
    elif cliArgs[0] == "-h":
        print("\nCommand List:")
        print("\t--store [TIME_MINUTES]: store brush time")
        print("\t--show: show daily brushing data\n")
    else:
        print("*** Unknown Command, run -h for information ***")
        return


# Run main when called
if __name__ == "__main__":
    main()
