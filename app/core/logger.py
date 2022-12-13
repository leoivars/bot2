# # -*- coding: UTF-8 -*-
import datetime
import os
import time

class Logger:
    ''' Losgs to a file keeping the last few lines in memory.
    '''
    
    def __init__(self, log_file_name=None,dirlogs=None,log_lines_to_keep_in_memory=200):
        ''' 
        initializes a logger setting default values in case they are not passed as parameters
        '''
        if dirlogs:
            self.dirlogs = dirlogs
        else:
            self.dirlogs = os.path.join( os.getcwd() ,os.getenv('DIR_LOGS', './logs/') )

        self.log_in_file= log_file_name != None                             #true will write log lines in file
        self.log_file_name = log_file_name
        self.nlog = self.dirlogs+log_file_name
        self.log_level = 2
        self.__log_lines_in_memory__ = []
        self.log_lines_to_keep_in_memory = log_lines_to_keep_in_memory
        self.update_time=time.time()

    def __del__(self):
        for l in  self.__log_lines_in_memory__:
            l = None
        del self.__log_lines_in_memory__  
        self.update_time=time.time()  

    def set_log_level(self,log_level):
        self.log_level = log_level

    def log(self,*args): 
        '''
           Logs all *args as a line  and writes to a file if loglevel > 1
        '''
        log_line = self.__build_log_a_line__(' '.join([str(a) for a in args]))
        self.__logmem__(log_line)
        if self.log_in_file and self.log_level > 1:
            self.__write_log_to_file__(log_line)
        print(log_line)

    def err(self,*args):
        '''
          Logs all *args  and writes to a file 
        '''
        log_line=self.__build_log_a_line__(' '.join([str(a) for a in args]))
        self.__logmem__(log_line)
        if self.log_in_file:
            self.__write_log_to_file__(log_line)
        time.sleep(0.01)

    def tail(self):
        ''' dump log lines keeped in memory
        '''
        txt=f'last {self.log_lines_to_keep_in_memory} lines of log:\n'
        for l in self.__log_lines_in_memory__:
            txt+=l
        return txt
    
    def __build_log_a_line__(self,line):
        ''' construct a log line adding date'''
        if self.log_level < 1:
            a='*'
        else:
            a=' '
        return datetime.datetime.now().strftime('%m%d %H:%M') + a + line+'\n'

    def __write_log_to_file__(self,log_line):
        ''' write log_line appening to a file
        '''
        try:
            flog=open(self.nlog,'a')
            flog.write(log_line)
            flog.close()
            time.sleep(0.001)
        except:
            print("can not write to log file:",self.nlog)
    
    def __logmem__(self,log_line):
        ''' append a lon_line to memory 
        '''
        self.update_time = time.time()
        self.__log_lines_in_memory__.append(log_line)
        if len(self.__log_lines_in_memory__) > self.log_lines_to_keep_in_memory:
            self.__log_lines_in_memory__[0]=None
            self.__log_lines_in_memory__.pop(0)  #elimina el primer elemento

    def get_update_time(self):
        return self.update_time    
    
