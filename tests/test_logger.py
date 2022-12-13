import unittest
import os 
import paths_for_tests
from app.core.logger import Logger

class Test_Logger(unittest.TestCase):
    def prepare_dir_and_file_for_test(self):
        self.dir_for_tests = '/tmp/test_logs/'
        self.log_file_name = 'test_log_file.log'
        self.full_log_name = os.path.join(self.dir_for_tests,self.log_file_name)    
        if not os.path.exists(self.dir_for_tests):
            os.makedirs(self.dir_for_tests)
        if os.path.exists(self.full_log_name):
            os.remove(self.full_log_name)    

    def log_file_has_text_in_line(self,text):
        ret = False
        with open(self.full_log_name, "r") as f:
            lines = f.readlines()
            f.close()
        for line in lines:
            if text in line:
                ret = True
                break
        return ret        

    def test_logger_creation(self):
        self.prepare_dir_and_file_for_test()
        log = Logger(self.log_file_name,self.dir_for_tests)
        test_line='test line 123456'
        log.log(test_line)
        self.assertTrue(  os.path.exists(self.full_log_name) )
        self.assertTrue( self.log_file_has_text_in_line(test_line))

    def test_logger_err(self):
        self.prepare_dir_and_file_for_test()
        log = Logger(self.log_file_name,self.dir_for_tests)
        test_line='test line 123456'
        log.set_log_level(0)
        log.err(test_line)
        self.assertTrue(  os.path.exists(self.full_log_name) )
        self.assertTrue( self.log_file_has_text_in_line(test_line))

    def test_logger_tail(self):
        self.prepare_dir_and_file_for_test()
        log = Logger(self.log_file_name,self.dir_for_tests,10)
        for i in range(1,30):
            log.log(f'test_line <{i}>')
        txt_tail = log.tail()
        print(txt_tail)
        self.assertTrue(  '<29>' in txt_tail )
        self.assertTrue(  '<20>' in txt_tail )
        self.assertFalse( '<19>' in txt_tail )


if __name__=='__main__':
    unittest.main()
