from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Iterable
import csv
import json
import logging
import math
import re
from collections import OrderedDict

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")


# Creating the validator

class Validator:
    REQUIRED_COLS = ["order_id", "timestamp", "item",  "payment_status"] # These are cols that are required to be present. Without any of them we would have to nullify that particular entry.
    OTHERS = ["quantity", "price","total"] # We require atleast two of the columns in this category to be present else we nullify the entire entry

    def __init__(self,
        min_quantity: int = 1.00,
        min_price: float = 0.10,
        min_total: float = 0.10):

        self.min_quantity = min_quantity
        self.min_price = min_price
        self.min_total = min_total

    """ TODO:  Ensures quantity, price, and total are present and positive. """

     
    def validate_rows_data(self, row: Dict[str, Any]): #  This would validate the rows after the dictionary is loaded as a list.
        if not isinstance(row, dict): #If the row is not a dictionary, then we log the message below and return None
            logger.debug("Row is not a dict, skipping: %s", row)
            return None
        
        for col in self.REQUIRED_COLS: # If any o fthe clumns in the REQUIRED_COLS list is not available that row will be dropped.
            if col not in row:
                logger.debug("Missing field %s in %s",col,row)
            return None 
        
        present = []
        for col in self.OTHERS:
            if col in row:
                present.append(col)
        if len(present) < 2:
            logger.warning("Insufficient numeric fields in row: %s", row)
            return None # Insufficient data
        else:
            return row
        
        
    def clean_float_entry(self,v: Any):
        if isinstance(v, (float, int)):
            return float(v)
        
        if isinstance(v, str):
            cleaned = re.sub(r"[^\d\.]", "", v)   
            try:
                float(cleaned)
            except ValueError:
                logger.debug("Failed to convert string to float: '%s'", v)
                return None
        else:
            logger.debug("Unsupported type for numeric cleaning: %s", type(v))
            return None 
        
    def clean_int_entry(self,v: any): # To be applied to the quantity column
        if isinstance(v, (float,int,bool)):
            return int(v)
        if isinstance(v, str):
            cleaned = re.sub(r"[^\d\.]","",v)
            try:
                int(cleaned)
            except ValueError:
                logger.debug("Failed to convert string to int: '%s'", v)
                return None
        else:
            logger.debug("Unsupported type for numeric cleaning: %s", type(v))
            return None   

         

































    # # A method that checks if a value is present and ensures it is in the right format
    # def _to_float(self, v: Any) -> Optional[float]:
    #     if v is None or v == "": # if the value passed in is None or an empty string
    #         return None # return None
    #     if isinstance(v, (int, float)) and not isinstance(v, bool): # check if it is an int or a float and not a booean 
    #         return float(v) # return the float 
    #     if isinstance(v, str): # if the value is a string
    #         try:
    #             return float(v) # ... Try to return the float of the value i.e convert it to a float
    #         except ValueError: # excepts it returns a value error then return None
    #             return None
    #     return None # if it is not a str just return None (might be other datatype not listed above)
    
    # def _to_int(self, v: Any):
    #     if v is None or v == "":
    #         return None
    #     if isinstance(v, (float,bool)):
    #         try:
    #             return int(v)
    #         except ValueError:
    #             return None
      


    # # validate strings
    # def validate_strings(self, v: str):
    #     pass

                