from datetime import datetime


class Shift:
    KNOWN_DEPTS = ['080/Cart Crew', '080/Self Check Out', '080/Member Service']

    def __init__(self, text):
        # Split info on \n token, and remove extra element of empty string
        textLines = text.split('\n')
        textLines.remove('')

        # First 2 elements are always the day of the week, and date of the shift.
        # This is true even for days off
        day = textLines[0]
        date = textLines[1]

        # If the 3rd element is an empty space, it means the day being examined is
        # an off day
        if textLines[2] == ' ':
            self.date = None
            return

        # Date will be listed twice on a line if the shift is split
        try:
            secondSplitStartIndex = textLines.index(date, 2)
        except ValueError:
            secondSplitStartIndex = -1

        start = textLines[2]

        if secondSplitStartIndex == -1:
            end = textLines[3]
        else:
            end = textLines[secondSplitStartIndex + 2]

        department = None
        for deptID in self.KNOWN_DEPTS:
            if deptID in textLines:
                # substring off the dept code, just get job title
                department = deptID[4:]

        self.day = day

        self.date = self.toRfcDate(date)
        self.start = self.toDatetime(start) 
        self.end = self.toDatetime(end)
        self.department = department
        self.event = self.createEvent()
        self.familyEvent = self.createEvent(family=True)

    def __str__(self):
        if self.date is None:
            return 'Day Off'

        toString = self.day + ' ' + self.date + ' ' + self.start.isoformat() + ' ' + self.end.isoformat()

        if self.department:
            toString += ' ' + self.department

        return toString

    def getDepartment(self):
        if self.department:
            return self.department
        else:
            return 'Front End'


    def toRfcDate(self, date):
        datePieces = date.split('/')

        month = datePieces[0]
        day = datePieces[1]
        year = datePieces[2]

        return year + '-' + month + '-' + day

    
    def toDatetime(self, time):
        # Get the individual pieces of the date 
        datePieces = self.date.split('-')
        year = int(datePieces[0])
        month = int(datePieces[1])
        day = int(datePieces[2])

        # Get the individual pieces of the time, change it to 24hr time
        timePieces = time.split(':')
        hour = int(timePieces[0])
        meridiem = time[-2:]
        if(meridiem == 'AM' and hour == 12):
            hour = 0
        elif(meridiem == 'PM' and hour != 12):
            hour += 12

        minute = int(timePieces[1][:2])

        return datetime(year, month, day, hour, minute)

    def createEvent(self, family=False):
        summary = 'Work - ' + self.getDepartment()
        if family:
            summary = 'Asa: ' + summary

        return {
            'summary': summary,
            'start': {
                'dateTime': self.start.isoformat(),
                'timeZone': 'America/Los_Angeles'
            },
            'end': {
                'dateTime': self.end.isoformat(),
                'timeZone': 'America/Los_Angeles'
            },
            'reminders': {
                'useDefault': True
            }
        }
