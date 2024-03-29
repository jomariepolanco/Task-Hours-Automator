# Connect to Google Calendar
# Connect to VS Code
# Determine start time in vscode
# Open directory/file in vscode
# Determine end time in vscode
# Git commit -m “” message
# Log difference on google calendar with project name as title

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from activities import Activities

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def post_gcal_event(activity):
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Posting event on Calendar...")
    for time in activity.time_entries:
      print(f"Time: { time.start_time.strftime('%Y-%m-%dT%H:%M:%S')}")
      event = {
          "summary": activity.title,
          "start": {
              "dateTime": time.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
              "timeZone": "America/Los_Angeles",
          },
          "end": {
              "dateTime": time.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
              "timeZone": "America/Los_Angeles",
          },
      }
      event = service.events().insert(calendarId="primary", body=event).execute()
      print(f"Event created: {event.get('htmlLink')}")

  except HttpError as error:
    print(f"An error occurred: {error}")