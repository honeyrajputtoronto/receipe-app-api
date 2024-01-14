"""Test custom django management command"""

#patch will be used to mock the behaviour of database to simulate the response of database
from unittest.mock import patch

#it's one of the possible error we might get when we try to connect with database before the databsae is ready
from psycopg2 import OperationalError as Psycopg2Error  # Corrected import

#It allows you to call Django management commands programmatically from within your Python code.
from django.core.management import call_command
# another exception that may get thrown by the database
from django.db.utils import OperationalError
# base test class which is going to be used for testing.
from django.test import SimpleTestCase

# we don't want it to do anything, we just want it to mock the behaviour of it. that's why we use patch
# patch method will be used to mock the behaviour and path is given for "Command" function with check method at end. which
# is a check method which allows to check the status of the database
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for the database if the database is ready"""

        #hardcoding the true value
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])


# this is used if the db is not ready yet and we'll add a delay and then check again
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
      """test waiting for database when gettting operational error"""
      # there are different stages of postgres first error represents that the application hasn't even started yet\
      # then second error is when database is ready to accept connections but it hasn't set up the testing database
      patched_check.side_effect = [Psycopg2Error] * 2 + \
        [OperationalError] * 3 + [True]

      call_command('wait_for_db')

      self.assertEqual(patched_check.call_count, 6)

      #patched_check.assert_called_once_with(database=['default']) is our way of
      # saying, "Hey, magical tool, check if we used our command wand exactly once,
      # and when we used it, did we say the magic words 'database=['default']'?"

      patched_check.assert_called_with(databases=['default'])