import uuid

def is_valid_uuid(uuid_to_test, version=4):
    """
    Checks that UUID is valid
    """
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
        return True
    except ValueError:
        return False