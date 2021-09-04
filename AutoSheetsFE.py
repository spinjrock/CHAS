#Spencer Oswald 9/3/21
from datetime import datetime, timedelta
from datetime import date
import SpreadsheetHandler
import SquareHandler

class AutoSheetFE:

    START_DATE: str
    END_DATE: str
    DATES = []
    SPREADSHEET_NAME: str

    def set_dates(self):
        repeat = True
        while repeat:
            start_date = input('What day would you like to start the search? (YYYY-MM-DD)\n')
            if start_date[4] == "-" and start_date[7] == "-":
                self.START_DATE = start_date
                repeat = False
            else:
                print("Incorrectly formatted start date, please format YYYY-MM-DD")
        repeat = True
        while repeat:
            end_date =  input('What day would you like to end the search? (YYYY-MM-DD)\n')
            if end_date[4] == "-" and end_date[7] == "-":
                self.END_DATE = end_date
                repeat = False
            else:
                print("Incorrectly formatted end date, please format YYYY-MM-DD")
    
    def set_spreadsheet_name(self):
        repeat = True
        while repeat:
            spreadsheet_name = input("What spreadsheet would you like to use?\nNote: If spreadsheet isn't found this will make a new one in current directory.\n")
            if spreadsheet_name != None and spreadsheet_name[len(spreadsheet_name)-5:len(spreadsheet_name)] == ".xlsx":
                self.SPREADSHEET_NAME = spreadsheet_name
                repeat = False
            else:
                print("Your spreadsheet file must be a .xlsx file, please try again.")

    def format_dates(self):
        start_date = self.START_DATE.split('-')
        end_date = self.END_DATE.split('-')
        start_date_obj = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
        end_date_obj = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
        date_delta = timedelta(days=1)
        while start_date_obj <= end_date_obj:
            self.DATES.append(str(start_date_obj))
            start_date_obj += date_delta

    def __main__(self):
        print('Welcome to Coffee House Auto Sheets!')
        self.set_dates()
        self.format_dates()
        self.set_spreadsheet_name()
        print("\n\nWorking...")
        SH = SquareHandler.SquareHandler(self.DATES)
        SH.generate_bodies()
        SPH = SpreadsheetHandler.SpreadsheetHandler(SH.get_range_totals(), self.SPREADSHEET_NAME)
        SPH.format_spreadsheet()
        SPH.write_spreadsheet()
        SPH.wrapup()
        print('Done!')

if __name__ == '__main__':
    AH = AutoSheetFE()
    AH.__main__()
    
        
        
        