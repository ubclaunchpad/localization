import uuid


def is_valid_uuid(uuid_string, version=4):
    """
    Checks that a string is a valid UUID
    """
    try:
        uuid_obj = uuid.UUID(uuid_string, version=version)
        return True
    except ValueError:
        return False
