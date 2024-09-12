import DBcall
from Analysis import analysis1
from Analysis2 import DataAnalysis
if __name__  == "__main__":
    DBcall.InsertJSONToMongo()
    DBcall.InsertCSVTODB()
    DBcall.ConvertJSONToCSV()
    analysis1()
    DataAnalysis()