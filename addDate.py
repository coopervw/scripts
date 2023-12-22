import os
from datetime import datetime

def add_date_to_file_names(file_path):
    for file_name in os.listdir(file_path):
        if os.path.isfile(os.path.join(file_path, file_name)):
            file_creation_time = datetime.fromtimestamp(os.path.getmtime(os.path.join(file_path, file_name)))
            new_file_name = file_creation_time.strftime('%Y-%m-%d') + ' ' + file_name
            os.rename(os.path.join(file_path, file_name), os.path.join(file_path, new_file_name))


