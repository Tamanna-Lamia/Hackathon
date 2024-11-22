def parse_file_name(file_name):
    file_name = file_name.split(".")[0]
    file_parts = file_name.split("_")
    file_details = {
        "school_name": file_parts[0],
        "data_Type" :  file_parts[1]
    }
    return file_details
