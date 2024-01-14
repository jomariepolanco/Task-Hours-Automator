import json 

class Activities:
    def __init__(self, activities):
        self.activities = activities
    
    def initialize(self):
        activities = Activities([])
        with open("activities.json", "w") as f:
            data = json.load(f)
            activities = Activities(self.get_activities(data))
        return activities
    
    def get_activities(self, data):
        activities_list = []
        for act in data["activities"]:
            activities_list.append(Activity(name=act["title"], time_entries=self.get_time_entries_for_activity(act["time_entires"])))
        return activities_list
    
    def get_time_entries_for_activity(self, time_entries):
        time_entries_list = []
        for entry in time_entries:
            time_entries_list.append(TimeEntry(time=entry["time"]))
        self.time_entries = time_entries_list
        return time_entries_list
    
    def serialize(self):
        return {"activities": self.make_activities_json()}
    
    def make_activities_json(self):
        activities = []
        for act in self.activities:
            activities.append(act.serialize())
        return activities
    

class Activity:
    def __init__(self, title, time_entries):
        self.title = title
        self.time_entries = time_entries
    
    def make_time_entries_json(self):
        time_list = []
        for time in self.time_entries:
            time_list.append(time.serialize())
        return time_list
    
    def serialize(self):
        return {"title": self.title, "time_entires": self.make_time_entries_json()}

class TimeEntry:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self.total_time = end_time - start_time
        self.days = (end_time - start_time).days
        self.hours = (end_time - start_time).days * 24 + (end_time - start_time).seconds % 60 // 3600
        self.seconds = (end_time - start_time).seconds % 60
        self.minutes = (end_time - start_time).seconds % 60 // 60
    
    def serialize(self):
        return {
            "start_time": self.start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "end_time": self.end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "total_time": self.total_time,
            "days": self.days,
            "hours": self.hours,
            "minutes": self.minutes,
            "seconds": self.seconds
        }