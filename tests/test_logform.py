import logging
import multiprocessing
import threading

# Our library.
from dls_logformatter.dls_logformatter import DlsLogform
from dls_logformatter.version import version

root_logger = logging.getLogger()


class Test_01:
    # -------------------------------------------------------------------------
    def test(self, output_directory):
        """
        Write single line to file and check that it is correct.
        """

        multiprocessing.current_process().name = "theprocess"
        threading.current_thread().name = "thethread"

        log_filename = "%s/logger.log" % (output_directory)

        try:
            # Make handler which writes the file, overwrite file if exists.
            handler = logging.FileHandler(log_filename, "w")

            # Make "long" type formatter.
            formatter = DlsLogform()

            # Let file handler write custom formatted messages.
            handler.setFormatter(formatter)

            # Let root logger use the file handler.
            root_logger.addHandler(handler)

            # Log level for all modules.
            root_logger.setLevel("DEBUG")

            # Log something.
            first_message = "logging_formatter version %s" % (version())
            root_logger.info(first_message)

            # Read the log file that has been written.
            with open(log_filename) as log_file:
                lines = log_file.readlines()

            # Check length of file.
            assert len(lines) == 1, "lines in log file %s" % (log_filename)

            # Parse the first line of the output file.
            parts = lines[0].split()

            assert parts[2] == str(multiprocessing.current_process().pid)
            assert parts[3] == multiprocessing.current_process().name
            assert parts[4] == threading.current_thread().name
            assert parts[7] == "INFO"

            module = parts[8]
            assert module[0] == "/", "first character of module is a slash"

            message = " ".join(parts[9:])
            assert message == first_message, "first message"
        finally:
            handler.close()
            root_logger.removeHandler(handler)


# -----------------------------------------------------------------------------
class Test_02:
    def test(self, output_directory):
        """
        Log a debug line followed by log an exception to file
        Check that file is correct.
        """
        multiprocessing.current_process().name = "theprocess"
        threading.current_thread().name = "thethread"

        try:
            # Make handler which writes the console.
            console_handler = logging.StreamHandler()

            # Make "short" type formatter.
            short_formatter = DlsLogform(type="short")

            # Let the console write the formatted messages.
            console_handler.setFormatter(short_formatter)

            log_filename = "%s/logger.log" % (output_directory)

            # Make handler which writes the file, overwrite file if exists.
            file_handler = logging.FileHandler(log_filename, "w")

            # Make "long" type formatter.
            long_formatter = DlsLogform()

            # Let file handler write custom formatted messages.
            file_handler.setFormatter(long_formatter)

            # Let root logger use the file handler.
            root_logger.addHandler(console_handler)
            root_logger.addHandler(file_handler)

            # Log level for all modules.
            root_logger.setLevel("DEBUG")

            root_logger.debug("hello")

            # Log the exception.
            first_exception = "first exception"
            try:
                self.raise_exception(first_exception)
            except Exception as exception:
                root_logger.exception(exception, exc_info=exception)

            # Read the log file that has been written.
            with open(log_filename) as log_file:
                lines = log_file.readlines()

            # Check length of file.
            assert len(lines) == 5, "lines in log file %s" % (log_filename)

            # -------------------------------------------------------
            # Parse the exception line of the output file.
            parts = lines[1].split()

            assert parts[2] == str(multiprocessing.current_process().pid)
            assert parts[3] == multiprocessing.current_process().name
            assert parts[4] == threading.current_thread().name
            assert parts[7] == "ERROR"

            module = parts[8]
            assert module[0] == "/", "first character of module is a slash"

            message = " ".join(parts[9:])
            assert message == first_exception, "first message"

            # -------------------------------------------------------
            # Parse the exception line of the output file.
            parts = lines[2].split()
            assert parts[0] == "EXCEPTION"

            assert parts[1] == "RuntimeError:"

            message = " ".join(parts[2:])
            assert message == "first exception"

            # -------------------------------------------------------
            # Parse the first traceback line of the output file.
            parts = lines[3].split()
            assert parts[0] == "TRACEBACK"

            module = parts[1]
            assert module[0] == "/", "line 2 first character of module is a slash"

            message = " ".join(parts[2:])
            assert message == "self.raise_exception(first_exception)", "first exception"

            # -------------------------------------------------------
            # Parse the second traceback line of the output file.
            parts = lines[4].split()
            assert parts[0] == "TRACEBACK"

            module = parts[1]
            assert module[0] == "/", "line 3 first character of module is a slash"

            message = " ".join(parts[2:])
            assert message == "raise RuntimeError(message)", "first exception"
        finally:
            file_handler.close()
            root_logger.removeHandler(file_handler)
            console_handler.close()
            root_logger.removeHandler(console_handler)

    # ------------------------------------------------------------------------
    def raise_exception(self, message):
        raise RuntimeError(message)


# -----------------------------------------------------------------------------
class Test_03:
    def test(self, output_directory):
        """
        Log an exception from a nested function.
        Write to file, and check tracebacks are correct.
        """
        multiprocessing.current_process().name = "theprocess"
        threading.current_thread().name = "thethread"

        try:
            # Make handler which writes the console.
            console_handler = logging.StreamHandler()

            # Make "short" type formatter.
            short_formatter = DlsLogform(type="short")

            # Let the console write the formatted messages.
            console_handler.setFormatter(short_formatter)

            log_filename = "%s/logger.log" % (output_directory)

            # Make handler which writes the file, overwrite file if exists.
            file_handler = logging.FileHandler(log_filename, "w")

            # Make "long" type formatter.
            long_formatter = DlsLogform()

            # Let file handler write custom formatted messages.
            file_handler.setFormatter(long_formatter)

            # Let root logger use the file handler.
            root_logger.addHandler(console_handler)
            root_logger.addHandler(file_handler)

            # Log level for all modules.
            root_logger.setLevel("DEBUG")

            root_logger.debug("hello")

            # Log the exception.
            first_stack = "first stack"
            self.log_to_stack(first_stack)

            # Read the log file that has been written.
            with open(log_filename) as log_file:
                lines = log_file.readlines()

            # Check length of file.
            assert len(lines) == 5, "lines in log file %s" % (log_filename)

            # -------------------------------------------------------
            # Parse the exception line of the output file.
            parts = lines[1].split()

            assert parts[2] == str(multiprocessing.current_process().pid)
            assert parts[3] == multiprocessing.current_process().name
            assert parts[4] == threading.current_thread().name
            assert parts[7] == "DEBUG"

            module = parts[8]
            assert module[0] == "/", "first character of module is a slash"

            message = " ".join(parts[9:])
            assert message == first_stack, "first message"

            module_index = lines[1].index("/")

            # -------------------------------------------------------
            # Parse the first traceback line of the output file.
            parts = lines[2][module_index:].split()

            module = parts[0]
            assert module[0] == "/", "line 2 first character of module is a slash"

            message = " ".join(parts[1:])
            assert message == "self.log_to_stack3(message)", "second message"

            # -------------------------------------------------------
            # Parse the second traceback line of the output file.
            parts = lines[3][module_index:].split()

            module = parts[0]
            assert module[0] == "/", "line 3 first character of module is a slash"

            message = " ".join(parts[1:])
            assert message == "self.log_to_stack2(message)", "third message"
        finally:
            file_handler.close()
            root_logger.removeHandler(file_handler)
            console_handler.close()
            root_logger.removeHandler(console_handler)

    # ------------------------------------------------------------------------
    def log_to_stack(self, message):
        self.log_to_stack2(message)

    # ------------------------------------------------------------------------
    def log_to_stack2(self, message):
        self.log_to_stack3(message)

    # ------------------------------------------------------------------------
    def log_to_stack3(self, message):
        root_logger.debug(message, stack_info=True)


# -----------------------------------------------------------------------------
class Test_04:
    def test(self, output_directory):
        """
        Raise an exception from a nested function.
        Write to file, and check tracebacks are correct.
        """
        multiprocessing.current_process().name = "theprocess"
        threading.current_thread().name = "thethread"

        try:
            log_filename = "%s/logger.log" % (output_directory)

            # Make handler which writes the file, overwrite file if exists.
            file_handler = logging.FileHandler(log_filename, "w")

            # Make "long" type formatter.
            long_formatter = DlsLogform()

            # Let file handler write custom formatted messages.
            file_handler.setFormatter(long_formatter)

            # Let root logger use the file handler.
            root_logger.addHandler(file_handler)

            # Log level for all modules.
            root_logger.setLevel("DEBUG")

            try:
                # Call the nesting.
                self.nest1()
            except Exception as exception:
                root_logger.error("error while calling nest1", exc_info=exception)
            # Read the log file that has been written.
            with open(log_filename) as log_file:
                lines = log_file.readlines()

            # Check length of file.
            assert len(lines) == 13, "lines in log file %s" % (log_filename)

            # -------------------------------------------------------
            # Parse the error line of the output file.
            parts = lines[0].split()

            assert parts[2] == str(multiprocessing.current_process().pid)
            assert parts[3] == multiprocessing.current_process().name
            assert parts[4] == threading.current_thread().name
            assert parts[7] == "ERROR"

            module = parts[8]
            assert module[0] == "/", "first character of module is a slash"

            message = " ".join(parts[9:])
            assert message == "error while calling nest1", "first message"

            module_index = lines[2].index("/")

            # -------------------------------------------------------
            # Parse the first exception line of the output file.
            parts = lines[1].strip().split()
            assert parts[0] == "EXCEPTION"

            message = " ".join(parts[1:])
            assert (
                message == "RuntimeError: exception while calling nest2"
            ), "first exception"

            # -------------------------------------------------------
            # Parse the first traceback line of the output file.
            parts = lines[2][module_index:].split()

            module = parts[0]
            assert module[0] == "/", "line 3 first character of module is a slash"

            message = " ".join(parts[1:])
            assert message == "self.nest1()", "second message"

            # -------------------------------------------------------
            # Parse the second traceback line of the output file.
            parts = lines[3][module_index:].split()

            module = parts[0]
            assert module[0] == "/", "line 4 first character of module is a slash"

            message = " ".join(parts[1:])
            assert (
                message == 'raise RuntimeError("exception while calling nest2")'
            ), "third message"

            # -------------------------------------------------------
            # Parse the second exception line of the output file.
            parts = lines[4].strip().split()
            assert parts[0] == "EXCEPTION"

            message = " ".join(parts[1:])
            assert (
                message == "RuntimeError: exception while calling nest3"
            ), "second exception"

        finally:
            file_handler.close()
            root_logger.removeHandler(file_handler)

    # ------------------------------------------------------------------------
    def nest1(self):
        try:
            self.nest2()
        except Exception:
            raise RuntimeError("exception while calling nest2")

    # ------------------------------------------------------------------------
    def nest2(self):
        try:
            self.nest3()
        except Exception:
            raise RuntimeError("exception while calling nest3")

    # ------------------------------------------------------------------------
    def nest3(self):
        try:
            self.nest4()
        except Exception:
            raise RuntimeError("exception while calling nest4")

    # ------------------------------------------------------------------------
    def nest4(self):
        if True:
            raise RuntimeError("exception inside nest4")
