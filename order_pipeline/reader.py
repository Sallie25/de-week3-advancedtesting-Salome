from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Iterable
import csv
import json
import logging
import math
from collections import OrderedDict

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

@dataclass   
class ShopLinkOrderRecord:
    order_id: str
    timestamp: str
    item: str
    quantity: int
    price: float
    total: float
    payment_status: str
    
    # A method that returns a dictionary
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
# Creating the reader class
class Reader:
    def __init__(self, path: str, format: str = "csv"):
        self.path = path
        self.format = format
        
    # Define a method that reads different file formats and passes them into a  dictionary
    def read(self) -> Iterable[Dict[str, Any]]:

        if self.format == "csv":
            with open(self.path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                     yield dict(row)

        elif self.format == "json":
            with open(self.path, "r", encoding="utf-8") as f:
                 data = json.load(f) # data is a list of dictionaries
                 for item in data:
                     yield item
        else:
            raise ValueError("Unsupported format: " + str(self.format))
