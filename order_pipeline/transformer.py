""" TODO: 
-Converts quantity, price, and total to numeric values.
-Normalizes payment_status (paid/pending/refunded → lowercase).
-Cleans text fields (trim spaces, fix casing).
-Recalculates total = quantity * price for consistency.

"""

from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")


# Create the Transformer class
class ShopLinkOrderTransformer:
    " Transform and clean Shoplink order data "
    def __init__(self, unique_fields=("order_id", "timestamp")): # unique_fields is a composite key initiated in the bid to identify duplicate entries
        self.unique_fields = unique_fields

    def transform(self, entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

        duplicate_count = 0
        cache = {}
        for entry in entries:
            values = []
            for col in self.unique_fields:
                value = getattr(entry,col) # returns each attribute
                values.append(value) # Add value to the values list
            composite_key = tuple(values) # Convert the list to a tuple. We use tuple because we would be using the composite key as a dictionary key late and tuples are appropriate unlike list as they are immutable unlike list
            if composite_key in cache:
                logger.info(f"Duplicate found for key {composite_key}, overwriting previous entry")
                duplicate_count += 1
            cache[composite_key] = entry # This will overwrite duplicates

            
        cleaned = []
        for data in cache.values():
            order_id = str(data.order_id)
            timestamp = str(data.timestamp)
            product = str(data.item)
            name = product.lower().strip() if isinstance(product, str) else None
            qty = round(float(data.quantity), 2)
            unit_cost = round(float(data.price), 2)
            bill = round(float(data.total), 2)
            payment_status = str(data.payment_status)

            cleaned.append({
                "order_id": order_id,
                "timestamp": timestamp,
                "item": name,
                "quantity": qty,
                "price": unit_cost,
                "total": bill,
                "payment_status": payment_status
            })

        return cleaned
