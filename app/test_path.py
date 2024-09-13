# test_path.py
import sys

def test_print_path():
    print(sys.path)
    assert 'fastapi' in sys.modules
