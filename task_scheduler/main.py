# Creating a Python command-line application that makes requests to the Google Calendar API.
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"] # read and write access to calendar


def main():
  
  creds = None
  ''' The file token.json stores the user's access and refresh tokens, and is
  created automatically when the authorization flow completes for the first
  time.'''
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token: 
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file("credentials.json",SCOPES)
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())


  try:
    service = build("calendar", "v3", credentials=creds)
    # *************creating events(writing into google calendar)*************
    events_result = {
                "summary":"my ace project",
                "location":"my house",
                "description":"task scheduler app",
                "colorId":"1",
                "start": {
                    "dateTime": "2023-12-27T04:00:00+05:30",
                    "timeZone": "Asia/Kolkata",
                },
                "end": {
                    "dateTime": "2023-12-31T04:00:00+05:30", # yyyy/mm/dd +time stamp+ utc offset
                    "timeZone": "Asia/Kolkata", #must match the time zone of your google calender
                },
                "recurrence": ["RRULE:FREQ=DAILY;COUNT=2"]
    }
    event = service.events().insert(calendarId="primary", body=events_result).execute()
    print("Event created: %s" % (event.get("htmlLink")))

    # *************listing events(reading from google calendar)*************
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")
    events_list = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_list.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])

  except HttpError as error:
    print(f"An error occurred: {error}")



if __name__ == "__main__":
  main()