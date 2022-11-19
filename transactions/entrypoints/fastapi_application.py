from fastapi import FastAPI, UploadFile, File

from transactions.bootstrap import bootstrap
from transactions.domain.commands import LoadTransactionsFromCSV
from transactions.views.sqlalchemy_transaction_views import SqlAlchemyTransactionViews

app = FastAPI()
bus = bootstrap()


@app.post("/transactions/load-csv")
def upload(file: UploadFile = File(...)):
    contents = [line.decode("utf-8") for line in file.file.readlines()]
    bus.handle(LoadTransactionsFromCSV(csv_content=contents))


@app.get("/transactions/balance")
def get_balance(account: str = None):
    """Get the transaction balance."""
    balances = [
        dict(account=account, balance=balance)
        for account, balance in SqlAlchemyTransactionViews().group_by_account(
            account=account
        )
    ]
    return {"data": balances}


@app.get("/transactions/monthly-balance")
def get_monthly_balance(account: str = None, month: int = None):
    """Get the transaction balance."""
    balances = [
        dict(account=account, balance=balance, date=date)
        for account, date, balance in SqlAlchemyTransactionViews().group_by_account_and_month(
            account=account,
            month=month,
        )
    ]
    return {"data": balances}
