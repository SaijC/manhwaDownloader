import logging
logging.basicConfig(level=logging.DEBUG)

myDict = {"tetsItems": [(1, "BLA1"), (2, "BLA2"), (3, "BLA3")]}

for a, b in myDict.items():
    logging.info(a)
    logging.info(b)
