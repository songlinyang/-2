import yaml
from utils.config import EXCEL_FILE
import openpyxl


class Util(object):
    def __init__(self):
        pass

    def xml_operate(self,filename):
        file = open(filename,"r")
        data = yaml.load(file)
        file.close()
        return data



    def excel_operate(filelocation):
        inwb = openpyxl.load_workbook(EXCEL_FILE)
        sheet = inwb.worksheets[0]
        data = sheet[filelocation].value
        return data

if __name__ == '__main__':
    A=Util.excel_operate('B2')
    print(A)
