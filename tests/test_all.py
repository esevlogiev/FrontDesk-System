import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tests.class_tests import *
from tests.validation_test import *
from tests.room_management_tests import *
from tests.test_client_management import *
from tests.test_reservation_management import *
from tests.test_maid_management import *
from tests.test_models import *

if __name__ == "__main__":
    unittest.main()