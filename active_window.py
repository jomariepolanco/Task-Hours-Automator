# monitor the site or app user is on 
from AppKit import NSWorkspace, NSAppleScript
import time 

active_window_name = None 
while True:
    new_window = (NSWorkspace.sharedWorkspace().activeApplication())
    current_window_name = new_window['NSApplicationName']

    if active_window_name is not current_window_name:
        active_window_name = current_window_name
        match active_window_name:
            # Google Chrome - get the url of the active tab as well
            case "Google Chrome":
                print(f"Current window: {active_window_name}")
                url_script = """tell app "google chrome" to get the url of the active tab of window 1"""
                script = NSAppleScript.initWithSource_(NSAppleScript.alloc(), url_script)
                url, err = script.executeAndReturnError_(None)
                if err:
                    raise Exception(err)
                
                print(f"Current tab url: {url.stringValue()}")
            case "Code":
                print(f"Current window: {active_window_name}")
            case None:
                raise Exception(f"Unknown window: {current_window_name}")
            case _:
                print(f"Current window: {active_window_name}")
            
    time.sleep(2)