import subprocess
import time
from datetime import datetime, timedelta


def run_script():
    try:
        subprocess.call(['python', 'your_script.py'])
    except Exception as e:
        print(f"An error occurred: {e}")


def wait_until_start(start_time):
    now = datetime.now()
    start_dt = datetime.combine(now.date(), start_time)

    # If start time is before the current time, start the next day
    if start_dt < now:
        start_dt += timedelta(days=1)

    wait_seconds = (start_dt - now).total_seconds()
    print(f"Waiting for {wait_seconds} seconds until start time...")
    time.sleep(wait_seconds)


def main(start_time, loop_hours:int, delay_hours:int):
    wait_until_start(start_time)

    delay_set = delay_hours*60

    for _ in range(loop_hours):  # Loop 10 times for 10 hours
        run_script()
        time.sleep(delay_set)  # Sleep for 1 hour (3600 seconds)


if __name__ == '__main__':
    # Set your desired start time here (2 minutes from now for testing)
    now = datetime.now()
    start_time = (now + timedelta(minutes=2)).time()
    main(start_time)
