from pymongo import MongoClient

def CreateClient():
    client = MongoClient() 
    client = MongoClient("mongodb+srv://aiarjun027:arjun1234@cluster0.beh4ixw.mongodb.net/timesheet?retryWrites=true&w=majority")
    db = client['timesheet']
    return db

if __name__ == '__main__':
    print(CreateClient())

