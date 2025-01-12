# =========================================================================== #
# Author: Omer Kemal                                                          #
# Social Media:                                                               #
#   - Facebook: https://web.facebook.com/omer.kemal.7                         #
#   - GitHub: https://github.com/omer-devil                                   #
# =========================================================================== #

from sqlalchemy.orm import sessionmaker

from database.modle import Assessment
from database.manage_db import Base
from utility.setting import Setting

# Set up a session for interacting with the database
Session = sessionmaker(bind=Base)
session = Session()

# Initialize settings and variables
var = Setting()
var.setting_var()


def getlist(s):
    """
    Processes a list of SQLAlchemy model objects, extracting relevant string
    information and splitting the string into a structured list of values.

    Args:
        s (list): List of SQLAlchemy model instances (e.g., `Assessment` objects).

    Returns:
        list: A list of lists, where each sublist contains strings parsed from the object string representations.
    """
    _filter = [str(info)[1:-1].split('-') for info in s]  # Split the string by '-' and store it in a list
    print(_filter)
    return _filter

def assessment_list(s):
    """
    Retrieves a list of all `Assessment` records from the database and processes
    them using the `getlist` function.

    Args:
        s (str): A string used for filtering the query, although it's currently unused.
    """
    # Query the `Assessment` table and get all records
    assessment = session.query(Assessment).filter_by().all()
    # Process the retrieved records into a structured list format
    getlist(assessment)
