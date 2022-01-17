import unittest, main

def test_test1():
    assert main.test() =='Pass!'

def test_test2():
    assert main.testDatabase() == 'Database Passed!'
    
if __name__ == "__main__":
    unittest.main()