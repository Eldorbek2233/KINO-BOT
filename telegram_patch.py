# Patch telegram library to avoid using imghdr
import sys

# Create mock imghdr module
class MockImghdr:
    def what(self, *args, **kwargs):
        return None

# Insert mock module into sys.modules
sys.modules['imghdr'] = MockImghdr()

# Now import the telegram module
import telegram
