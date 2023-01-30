import re
from typing import Any, List, cast

# ------------------------------------------------------------------------
ansi_colors_regex = re.compile(
    r"(?:\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])"
)


def flatten_exception_message(exception: BaseException) -> str:
    """
    Remove newlines from certain package exception messages.

    This function knows how to flatten messages from certain external packages.

    Currently these are: PyTango and Jupyter nbconvert.

    Does not import these packages, insteads bases discovery on class type name.
    """

    # We don't really know what type of exception it is.
    cast_exception = cast(Any, exception)

    # Get the informative part of a tango exception.
    if type(cast_exception).__name__ in [
        "DevFailed",
        "ConnectionFailed",
        "CommunicationFailed",
    ]:
        try:
            message = cast_exception.args[0].desc.rstrip().replace("\n", " ")
        except Exception as exception2:
            message = str(exception2)

    # Get the informative part of a particular Jupyter nbconvert error.
    elif type(cast_exception).__name__ in ["CellExecutionError"]:
        cell_line = None
        # Jupyter ExecutePreprocessor traceback is a multi-line string.
        lines = cast_exception.traceback.split("\n")
        for line in lines:
            # Remove colorization that jupyter puts in these messages.
            line = ansi_colors_regex.sub("", line)
            # This is the line in the traceback with the cell error?
            if line.startswith("Input In ["):
                cell_line = line
                break

        if hasattr(cast_exception, "ename"):
            ename = cast_exception.ename
            evalue = cast_exception.evalue
        else:
            ename = type(cast_exception).__name__
            evalue = "in a cell, please refer to the .ipynb or .html file"

        # Be tolerant of traceback not providing the cell.
        if cell_line is None:
            message = "%s %s" % (ename, evalue)
        else:
            message = "%s in %s: %s" % (ename, cell_line, evalue)
    else:
        message = str(cast_exception)

    return message


# ------------------------------------------------------------------------
def list_exception_causes(exception: BaseException) -> List[str]:
    """
    Recurse through the cause chain, making
    an array of lines by appending the exception message
    with the causing exceptions' messages.

    """

    # Remove newlines from exception message.
    message = flatten_exception_message(exception)

    cause_list = ["%s: %s" % (type(exception).__name__, message)]
    if exception.__cause__ is not None:
        cause_list.extend(list_exception_causes(exception.__cause__))
    elif exception.__context__ is not None:
        cause_list.extend(list_exception_causes(exception.__context__))

    return cause_list


# ------------------------------------------------------------------------
def format_exception_causes(exception: BaseException, join_string="... ") -> str:
    """
    Make a single string by joining the exception message
    with the causing exceptions' messages.

    Typically used when a the message is intended for a
    display mechanism known not to show a multiline message very well,
    such as some Tango's Jive and other MsgBox type dialogs.
    """

    return join_string.join(list_exception_causes(exception))
