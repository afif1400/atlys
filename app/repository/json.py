import json
from typing import List
from pathlib import Path
from app.models.product import Product

class JSONRepository:
    def __init__(self, file_path: str = "db.json"):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            self.file_path.write_text("[]")

    def get_all(self) -> List[Product]:
        with self.file_path.open() as f:
            return [Product(**item) for item in json.load(f)]

    def update(self, products: List[Product]):
        with self.file_path.open("w") as f:
            json.dump([product for product in products], f, indent=4)
