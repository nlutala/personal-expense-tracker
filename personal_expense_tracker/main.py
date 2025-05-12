from typing import Union

from fastapi import FastAPI

app = FastAPI()


# Get the categories and the spending budget for categories
@app.get("/")
def read_root():
    return {
        "Subscriptions": 50,
        "Groceries": 200,
        "Entertainment": 100,
        "Transportation": 150,
    }

# TODO: Add a new category... Will revisit this later
@app.get("/add_category/{category_name}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
