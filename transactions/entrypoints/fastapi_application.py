from fastapi import FastAPI, UploadFile, File

from transactions.bootstrap import bootstrap
from transactions.domain.commands import LoadTransactionsFromCSV
from transactions.views.transaction_view_factory import TransactionViewFactory

app = FastAPI()
app.bus = bootstrap()


@app.post("/transactions/load-csv")
def upload(file: UploadFile = File(...)):
    contents = [line.decode("utf-8") for line in file.file.readlines()]
    app.bus.handle(LoadTransactionsFromCSV(csv_content=contents))


@app.get("/transactions/balance")
def get_balance(account: str = None):
    """Get the transaction balance."""
    view = TransactionViewFactory.from_config()
    balances = [
        dict(account=account, balance=balance)
        for account, balance in view.group_by_account(account=account)
    ]
    return {"data": balances}


@app.get("/transactions/monthly-balance")
def get_monthly_balance(account: str = None, month: int = None):
    """Get the transaction balance."""
    view = TransactionViewFactory.from_config()
    balances = [
        dict(account=account, balance=balance, date=date)
        for account, date, balance in view.group_by_account_and_month(
            account=account,
            month=month,
        )
    ]
    return {"data": balances}
