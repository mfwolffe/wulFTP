import logging


def init_logging(log_file="sftp.log", console_level=logging.WARNING, file_level=logging.DEBUG):
    """
      Create and configure a logger with distinct
      handlers for console and logfile
    """
    # DONE? @mfwolffe jump table for log methods
    #                maybe enum for readability
    #
    # NOTE:          ^ I think we can use the logging
    #                  module's constants actually?
    #
    # NOTE: by default getlogger will create or retrieve a socalled
    #       'named logger' which allows for referencing a logger across files
    #       if the logger exists, it just retrieves it
    #
    logga = logging.getLogger("sftp_logger")

    # NOTE: maybe counterintuitive but the logger
    #       will not propagate anything itself does not
    #       capture, so in order for both handlers (below)
    #       to behave, logga's gotta capture minimum set accepted
    #       by the handla's
    #
    logga.setLevel(logging.DEBUG)

    # logging to both console and a file I believe
    # requires this approach of multiple handlers
    # NOTE: console handler ignores INFO dispatches
    #       file handler accepts everything 
    #
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))

    file_handler = logging.FileHandler('sftp.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s"))

    logga.addHandler(file_handler)
    logga.addHandler(console_handler)

    return logga


def dispatch(level: int, msg: str, err=None):
    """
      Log a message at a given level with
      preconfigured logger
    """
    logga = logging.getLogger("sftp_logger")
    out = f"{msg}: {err}" if err else msg

    loggers = {
        logging.INFO:     logga.info,
        logging.DEBUG:    logga.debug,
        logging.ERROR:    logga.error,
        logging.WARNING:  logga.warning,
        logging.CRITICAL: logga.critical,
    }

    # NOTE: fallback to INFO on bad loglevel
    #
    if not isinstance(level, int) or level not in loggers:
        logga.warning(f"Invalid log level ({level}) used in dispatch. Falling back to INFO")
        level = logging.INFO

    # NOTE: overloaded get defaults to arg2
    #       if key not found
    #
    # NOTE: check on level in bound above
    #       allows lookup without getter 
    #
    # old: loggers.get(level, logga.info)(out)
    loggers[level](out)


# SEVERETIES = {0: "Fatal", 1: "Error", 2: "Warning", 3: "Internal", 4: "Info"}
# def dispatch(level: int, msg: str, err=None):
    # print(f"[{SEVERETIES[level]}] {msg}: {'' if err is None else err}")
