# monitor the site or app user is on 
import json
from AppKit import NSWorkspace, NSAppleScript
import time 
import datetime

from activities import Activities, TimeEntry, Activity
from gcal import post_gcal_event

active_window_name = None 
activity_title = None 
start_time = datetime.datetime.now()
activity_list = Activities([])
first_time = True

def get_active_window_name():
    return (NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName'])

def get_window_url():
    url_script = """tell app "google chrome" to get the url of the active tab of window 1"""
    script = NSAppleScript.initWithSource_(NSAppleScript.alloc(), url_script)
    url, err = script.executeAndReturnError_(None)
    if err:
        raise Exception(err)
                
    return url.stringValue()

try: 
    activity_list.initialize()
except Exception:
    print("No activities.json file found")

try:
    while True:
        previous_window = None 
        new_window_name = get_active_window_name()
        match new_window_name:
            case "Google Chrome":
                new_window_name = get_window_url()
            # TODO: add more cases here
    
        if active_window_name != new_window_name:
            print(f"windows: {active_window_name} -> {new_window_name}")
            activity_title = active_window_name
        
            if not first_time:
                end_time = datetime.datetime.now()
                time_entry = TimeEntry(start_time, end_time)

                exists = False
                for act in activity_list.activities:
                    if act.title == activity_title:
                        exists = True
                        act.time_entries.append(time_entry)

                if not exists:  
                    activity = Activity(activity_title, [time_entry])
                    activity_list.activities.append(activity)
                    post_gcal_event(activity)
                
                with open("activities.json", "w") as json_file:
                    json.dump(activity_list.serialize(), json_file, indent=4, sort_keys=True, default=str)
                    start_time = datetime.datetime.now()
        
            first_time = False
            active_window_name = new_window_name

        time.sleep(1)

except KeyboardInterrupt:
    with open("activities.json", "w") as json_file:
        json.dump(activity_list.serialize(), json_file, indent=4, sort_keys=True, default=str)
