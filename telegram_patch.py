# Patch telegram library to avoid using imghdr and fix urllib3 issues
import sys
import importlib.util

# Create mock imghdr module
class MockImghdr:
    def what(self, *args, **kwargs):
        return None

# Insert mock module into sys.modules
sys.modules['imghdr'] = MockImghdr()

# Check if urllib3 is installed
try:
    import urllib3
except ImportError:
    # If urllib3 is not installed, create a mock package
    class MockUrllib3:
        def __init__(self):
            self.request = type('Request', (), {})
            self.vendor = type('Vendor', (), {'ptb_urllib3': type('ptb_urllib3', (), {'urllib3': self})})

    # Create mock urllib3 module
    mock_urllib3 = MockUrllib3()
    sys.modules['urllib3'] = mock_urllib3

    # Also mock vendor modules
    vendor_module = type('vendor_module', (), {})
    vendor_module.ptb_urllib3 = type('ptb_urllib3', (), {})
    vendor_module.ptb_urllib3.urllib3 = mock_urllib3
    sys.modules['telegram.vendor.ptb_urllib3.urllib3'] = mock_urllib3
    sys.modules['telegram.vendor.ptb_urllib3'] = vendor_module.ptb_urllib3
    sys.modules['telegram.vendor'] = vendor_module

# Now import the telegram module
try:
    import telegram
    print("Successfully imported telegram")
except Exception as e:
    print(f"Error importing telegram: {str(e)}")
