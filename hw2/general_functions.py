


def read_file_contents(file_name=None):
    """This function is used to read the file contents and return contents
    in a string format.
    Args:
        file_name: file which need to be read.
    Returns:
        SUCCESS when successfully read else FAILURE
        file_content: Complete content of file.
    Raises:
        NA.
    """
    if file_name is None:
        return False, 'NA'

    try:
        file_descriptor = open(file_name, "rb")
    except IOError:
        logging.error("Unable to open given protobuf file")
        return False, 'NA'

    file_content = file_descriptor.read()
    file_descriptor.close()
    return True, file_content

