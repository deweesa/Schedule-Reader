from PyPDF2 import PdfFileReader
from Shift import Shift
import os


def main():
    shifts = getShifts()
    print(shifts)
    print('finish')


def getShifts():
    rootDirectory = 'D:\\Projects\\Schedule Reader\\'
    newScheduleDirectory = os.path.join(rootDirectory, 'Schedules')
    oldScheduleDirectory = os.path.join(newScheduleDirectory, 'Old Schedules')

    shifts = []
    for filename in os.listdir(newScheduleDirectory):
        if filename.endswith('.pdf'):
            path = os.path.join(newScheduleDirectory, filename)
            newShifts = readSchedule(path)
            shifts.extend(newShifts)
            os.rename(path, os.path.join(oldScheduleDirectory, newShifts[0].date+'.pdf'))
        else:
            continue
    
    return shifts


def readSchedule(schedulePath):
    with open(schedulePath, 'rb') as f:
        fullSchedule = getText(f)
        f.close()

    shiftTextList = getShiftTextList(fullSchedule)

    shifts = []
    for textShift in shiftTextList:
        shifts.append(Shift(textShift))

    removeDaysOff(shifts)

    for shift in shifts:
        print(shift)

    return shifts


def getText(f):
    pdf = PdfFileReader(f)
    page = pdf.getPage(0)
    return page.extractText()


def getShiftTextList(schedule):
    weekdays = ['Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday', 'Sunday', 'Total']
    shiftTexts = []

    for i in range(len(weekdays)-1):
        startIndex = schedule.find(weekdays[i])
        endIndex = schedule.find(weekdays[i+1])

        shift = schedule[startIndex:endIndex]
        shiftTexts.append(shift)

    return shiftTexts


def removeDaysOff(shifts):
    i = 0
    while i < len(shifts):
        shift = shifts[i]
        if shift.date is None:
            shifts.remove(shift)
            i -= 1

        i += 1


if __name__ == '__main__':
    main()
