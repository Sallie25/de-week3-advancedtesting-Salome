import re
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")


OTHERS = ["quantity", "price","total"]
row = ["price"]

present = []
for col in OTHERS:
    if col in row:
        present.append(col)
if len(present) < 2:
    print(None)   

# Testing float type conversion logic

v = input("Enter value to test block of code logic:")
if isinstance(v, (float, int)):
    print (float(v))

if isinstance(v, str):
    cleaned = re.sub(r"[^\d\.]", "", v)   
    try:
        float(cleaned)
        print(type(cleaned))
    except ValueError:
        logger.debug("Failed to convert string to float: '%s'", v)
        print(None)
else:
    logger.debug("Unsupported type for numeric cleaning: %s", type(v))
    print(None) 