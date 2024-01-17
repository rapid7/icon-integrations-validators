NO_LOCAL_CON_VERSION = "Connection detail specified in plugin.spec.yaml but no connection version has been specified."
NO_CON_VERSION_CHANGE = "Connection details have changed but no version bump has occurred."
INVALID_CON_VERSION_CHANGE = "Connection details have not changed but the connection version was bumped."
INCORRECT_CON_VERSION_CHANGE = "Connection version has been bumped incorrectly."
FIRST_TIME_CON_VERSION_ISSUE = "First time connection version is supplied does not match expected value."

class ValidationException(Exception):
    """
    An exception which indicates that a validator has failed
    """
    # TODO report back which validator rule failed
    pass
