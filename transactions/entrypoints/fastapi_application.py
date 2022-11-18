from fastapi import FastAPI, UploadFile, File

from transactions.bootstrap import bootstrap
from transactions.domain.commands import LoadTransactionsFromCSV

app = FastAPI()
bus = bootstrap()


@app.post("/transactions/load-csv")
def upload(file: UploadFile = File(...)):
    contents = [line.decode("utf-8") for line in file.file.readlines()]
    bus.handle(LoadTransactionsFromCSV(csv_content=contents))
