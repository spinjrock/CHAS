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
        #TODO Input validation
        self.START_DATE = input('What day would you like to start the search? (YYYY-MM-DD)\n')
        self.END_DATE =  input('What day would you like to end the search? (YYYY-MM-DD)\n')

    def set_spreadsheet_name(self):
        #TODO Input validation
        self.SPREADSHEET_NAME = input("What spreadsheet would you like to use?\nNote: If spreadsheet isn't found this will make a new one in current directory.\n")

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
    
        
        
        