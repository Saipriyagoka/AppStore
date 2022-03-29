import uuid
from pydantic import BaseModel
from typing import List, Optional
from fastapi import Request

class CommodityBase(BaseModel):
    item: str
    itemCategory: str
    quantity: int
    price: int

class CommodityList(BaseModel):
    items: List[CommodityBase] 

class ProductCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.item: Optional[str] = None
        self.item_category: Optional[str] = None
        self.quantity: Optional[int] = None
        self.price: Optional[int] = None

    async def load_data(self):
        form = await self.request.form()
        self.item_id = str(uuid.uuid4)
        self.item = form.get("item")
        self.item_category = form.get("item_category")
        self.quantity = form.get("quantity")
        self.price = form.get("price")
        self.product = {
            'item': self.item,
            'item_category': self.item_category,
            'quantity': int(self.quantity),
            'price': int(self.price)
        }

    def is_valid(self):
        if not self.item:
            self.errors.append("A valid item is required")
        if not self.item_category:
            self.errors.append("Item Category is required")
        if not self.quantity:
            self.errors.append("Qunatity is required")
        if not self.price:
            self.errors.append("Price si required")
        if not self.errors:
            return True
        return False