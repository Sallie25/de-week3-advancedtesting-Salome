from typing import List, Dict, Any, Optional, Iterable
import logging
import re
from datetime import datetime
from reader import ShopLinkOrderRecord

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

    

     
    def validate_rows_data(self, row: Dict[str, Any]): #  This would validate the rows after the dictionary is loaded as a list.
        """ This method checks the presence of each columns """

        if not isinstance(row, dict): #If the row is not a dictionary, then we log the message below and return None
            logger.debug("Row is not a dict, skipping: %s", row)
            return None
        
        for col in self.REQUIRED_COLS: # If any of the columns in the REQUIRED_COLS list is not available that row will be dropped.
            if col not in row:
                logger.debug("Missing field %s in %s",col,row)
            return None 
        
        present_row = []
        for col in self.OTHERS:
            if col in row:
                present_row.append(col)
        if len(present_row) < 2:
            logger.warning("Insufficient numeric fields in row: %s", row)
            return None # Insufficient data
        else:
            return row
        

        
    # Normalizing the data type format of float values
    def clean_float_entry(self,v: Any):

        """ This method checks the validity of the entries by implementing the appropriate data type"""

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

    # Normalizing the data type format of integer values like quantity  
    def clean_int_entry(self,v: any): 
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

    # Normalizing the data type format of Timestamps
    def validating_timestamps(self, ts: str):
        """Normalize timestamp to ISO 8601 format: YYYY-MM-DDTHH:MM:00Z"""
        formats = [
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%d %H:%M",
            "%d/%m/%Y %I:%M %p",
            "%Y/%m/%dT%H:%MZ"
        ]
        for fmt in formats:
            try:
                dt = datetime.strptime(ts, fmt) # If "ts" matches "fmt", then return a datetime.datetime object and assign it to "dt"
                return dt.strftime("%Y-%m-%dT%H:%M:00Z")
            except ValueError:
                continue
        logger.warning("Unrecognized timestamp format: '%s'", ts) # After going through all the available formats to check and still not finding a suitable format then, return None
        return None
    
     # Normalizing the data type format of strings
    def norm_str(self, v: any):
        if not isinstance(v, str):
            return None


    # Validating all field entries
    def validate_entries(self, entry: Dict[str, Any]) -> Optional[Dict[str, Any]]: # Entry here, refers to a row of data
        """ This method implements the data type validation checks by checking each entry """

        # validate order_id entries
        order_id = entry.get("order_id") # Get the value associated with this key "order_id"
        if not re.fullmatch(r"ORD\d+", str(order_id)):
            logger.warning("Invalid order_id format: '%s'", order_id)
            return None
        
        # Validate timestamp entries
        timestamp = self.validating_timestamps(entry.get("timestamp",""))
        if not timestamp:
            logger.warning("Invalid timestamp in record: %s", entry)
            return None
        
        # Validate item entries
        item = self.norm_str(entry.get("item",""))
        if not item:
            logger.warning("Missing or invalid item field: '%s'", item)
            return None  
        
        # Validate Numeric entries
        quantity = self.clean_int_entry(entry.get("quantity"))
        price = self.clean_float_entry(entry.get("price"))
        total = self.clean_float_entry(entry.get("total"))

        if any([
            quantity is not None and quantity < self.min_qty,
            price is not None and price < self.min_price,
            total is not None and total < self.min_total
            ]):
            logger.info("Record rejected due to values below thresholds: %s", entry)
            return None
        
        #  What to do we two of the values in this list is available - "quantity", "price", "total"
        values = {"quantity": quantity, "price":price, "total":total}

        present_values = []
        for key, value in values.items():
            if value is not None:
                present_values.append(key)

        if len(present_values) < 2:
            logger.warning("Not enough numeric values to compute missing field: %s", entry)
            return None  

        try:
            if quantity is None:
                quantity = total / price
                logger.debug("Computed missing quantity: %.2f", quantity)
            elif price is None:
                price = total / quantity
                logger.debug("Computed missing price: %.2f", price)
            elif total is None:
                total = quantity * price
                logger.debug("Computed missing total: %.2f", total)

        except Exception as e:
            logger.error("Error computing missing value: %s",e)
            return None     
             
        
        # validate payment_status
        status = self.norm_str(entry.get("payment_status","")).strip().lower() # it fetches the payment status except if it is missing then it will return an empty string instead of a key error. Using type hint at the defination of this method made this easy to achieve.

        if status not in ["paid", "refunded", "pending"]:
            logger.warning("Invalid payment_status: '%s'", status)
            return None 

        # Assigning validated columns and entries to a new dictionary called data_row

        data_row = {
            "order_id": order_id,
            "timestamp": timestamp,
            "item": item,
            "quantity": round(quantity, 2),
            "price": round(price, 2),
            "total": round(total, 2),
            "payment_status": status
             }
        
        logger.info("Validated record: %s", data_row)

        cleaned_data = ShopLinkOrderRecord(order_id = data_row["order_id"],
                                     timestamp = data_row["timestamp"],
                                     item = data_row["item"],
                                     payment_status = data_row["payment_status"],
                                     quantity = data_row["quantity"],
                                     price = data_row["price"],
                                     total = data_row["total"])
        return cleaned_data






























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

                