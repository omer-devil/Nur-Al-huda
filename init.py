# =========================================================================== #
# Author: Omer Kemal                                                          #
# Social Media:                                                               #
#   - Facebook: https://web.facebook.com/omer.kemal.7                         #
#   - GitHub: https://github.com/omer-devil                                   #
# =========================================================================== #

from database.manage_db import create_db_dir, create_all_db_tables, create_admin_account, create_log_dir, engine, default_subject,create_excel_dir

# creating db dir if not exist
print(create_db_dir())
# creating database and creating all table
print(create_all_db_tables(engine))
# create admin account
create_admin_account(engine)
# creating log dir if not exist
print(create_log_dir())
# creating excel dir if not exist
print(create_excel_dir())
if input('Do you want to insert default available subjects(y/n)? ').lower() == 'y':
    print(default_subject(engine))
