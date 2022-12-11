# # -*- coding: UTF-8 -*-
from app.market_reader.candlestick import Candlestick
from app.market_reader.clandlestick_list_constants import *
#import numpy as np
import pandas as pd
import time
from threading import Lock

class Candlestick_Set:
    
    #proxima_vela={}
    def __init__(self,candlestick_list=None,size=200): 
        
        ''' receives an initial set of candlestick_list and the number of candlestick_list to memorize.

        :candlestick_list [list,list] a list candlestick [ [ open_time, open, high ,low, close, volume, close_time,ather fields ignored...], [open_time,...], ...  ] 
          example = [ [1670299200000, '17003.84000000', '17023.41000000', '16955.13000000', '17001.17000000', '27028.21636000', 1670313599999, '459394516.64545470', 559525, '13273.58246000', '225615357.19813410', '0'],
                      [1670313600000, '17001.17000000', '17041.96000000', '16906.37000000', '16983.90000000', '37036.12495000', 1670327999999, '629096324.31967460', 786549, '18216.08824000', '309431126.45219650', '0']
                          ] 
        :size int number of candlesticks keep in this set                  

        '''

        self.size=size                                 # the quantity of  candlesicks stores y this set  
        self.updating = Lock()                         # Lock for prevent access to other threads whiele updating
        self.update_time = 0
        
        self.new_set(candlestick_list)

    def lock_for_acess(func):
        ''' decorator that adds self.updating.acquire(True) and self.updating.release() to the method applied. 
        '''
        def wrapper(self,*args, **kwargs):
            self.updating.acquire(True) 
            ret = func(self,*args, **kwargs)
            self.updating.release()
            return ret
        
        return wrapper       
        
    
    def new_set(self,candlestick_list):
        ''' Creates a new data set with the list indicated as a parameter'''
        try:
            self.__create_new_dataframe()
            if candlestick_list:
                self.update_from_candlestick_list(candlestick_list)
        except Exception as e:
            print(str(e))
    @lock_for_acess
    def __create_new_dataframe(self):
        ''' Creates an empty dataframe for store candlestick_set
        '''
        self.df=pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume','close_time','closed'] )   

    @lock_for_acess
    def set_update_time_to_actual_time(self):
        self.update_time = time.time() 
        
    # @lock_for_acess
    # def update_from_cursor(self,cursor):
    #     ''' updates candlestick_set from db cursor
    #     '''
    #     for row in cursor:
    #         v_open_time=int(row[1])
    #         v_open=float(row[2])
    #         v_high=float(row[3])
    #         v_low=float(row[4])
    #         v_close=float(row[5])
    #         v_volume=float(row[6])
    #         v_close_time=int(row[7])
    #         self.df.loc[v_open_time] = [v_open ,v_high ,v_low ,v_close ,v_volume,v_close_time,1]
    #     self.___release_exceeded_data()
    #     self.update_time = time.time()
        
    @lock_for_acess
    def update_from_candlestick_list(self,candlestick_list):
        ''' Updates the candlestick_set getting values from a candlestick_list
        '''
        
        for candlestick in (candlestick_list):
            v_open_time=int(candlestick[OPEN_TIME])
            v_open=float(candlestick[OPEN])
            v_high=float(candlestick[HIGH])
            v_low=float(candlestick[LOW])
            v_close=float(candlestick[CLOSE])
            v_volume=float(candlestick[VOLUME])
            v_close_time=int(candlestick[CLOSE_TIME])
            self.df.loc[v_open_time] = [v_open ,v_high ,v_low ,v_close ,v_volume,v_close_time,1]
        self.___release_exceeded_data()
        self.update_time = time.time()
        
    @lock_for_acess
    def update(self,v_open_time,v_open,v_high,v_low,v_close,v_volume,v_close_time,v_is_closed):
        ''' Updates the candlestick_set getting values by separated paramemeters
        '''
        try:
            self.df.loc[int(v_open_time)] = [float(v_open) ,float(v_high) ,float(v_low) ,float(v_close) ,float(v_volume),int(v_close_time),v_is_closed] 
            
            if v_is_closed:                               
                self.___release_exceeded_data()

            self.update_time = time.time()     

        except Exception as e:
            
            print(str(e))
    
    def ___release_exceeded_data(self):
        '''adjusts the amount of candesticks in memory to respect the size set by self.size
           !! This method must called inside function that previusley did self.updating.acquire
        '''     
        quantity_exceeded = len(self.df) - self.size
        if quantity_exceeded > 0 :
            self.df.drop( self.df.index[:quantity_exceeded], inplace=True)

    def __i_from_end(self,qty_values):  #i_desde_final
        '''translate qty_values to -i position for get last qty_values
           !! This method must called inside function that previusley did self.updating.acquire
        '''     
        if qty_values is None:            #None, means all
            i =  (len(self.df))
        elif qty_values > len(self.df):   #More than len(df) --> all
            i =  (len(self.df))
        else:
            i =  qty_values
            
        return i * -1   

    @lock_for_acess
    def values_np_high(self,qty_values=None):  #valores_np_high
        '''return a numpy list of last qty_values high  '''
        i = self.__i_from_end(qty_values)
        ret = self.df['high'].iloc[i:].to_numpy()
        return ret

    @lock_for_acess
    def values_np_low(self,qty_values=None):  #valores_np_low
        '''return a numpy list of last qty_values low  '''
        i = self.__i_from_end(qty_values)
        ret = self.df['low'].iloc[i:].to_numpy()
        return ret

    @lock_for_acess
    def values_np_open(self,qty_values=None): #valores_np_open
        '''return a numpy list of last qty_values open  '''
        i = self.__i_from_end(qty_values)
        ret = self.df['open'].iloc[i:].to_numpy()
        return ret

    @lock_for_acess
    def values_np_close(self,qty_values=None):
        '''return a numpy list of last qty_values close  '''
        
        i = self.__i_from_end(qty_values)
        ret = self.df['close'].iloc[i:].to_numpy()
        return ret

    @lock_for_acess
    def values_np_volume(self,qty_values=None):
        '''return a numpy list of last qty_values volume  '''
        
        i = self.__i_from_end(qty_values)
        ret = self.df['volume'].iloc[i:].to_numpy()
           
        return ret

    @lock_for_acess
    def panda_df(self,qty_values=None):
        '''return a pandas dataframe with last qty_values  '''
        ret = self.df.tail(qty_values)
        return ret

    @lock_for_acess
    def last_candlestick(self):
        '''return the last candlestik closed or not '''
        return Candlestick( self.df.iloc[ -1 ], self.df.index[-1] )
    
    @lock_for_acess
    def last_closed_candlestick(self):
        '''return the last closed candlestick '''
        if self.df.iloc[-1]["closed"]:
            closed_candlestick = Candlestick( self.df.iloc[ -1 ], self.df.index[-1] )
        else:
            closed_candlestick = Candlestick( self.df.iloc[ -2 ], self.df.index[-2] )   
        
        return closed_candlestick
        
    @lock_for_acess
    def get_candlestick_from_end(self,pos):
        '''returns the candlestick in the position pos from the end of data. pos=1 is the last available candlestick '''
       
        return Candlestick( self.df.iloc[ pos * -1 ] , self.df.index[ pos * -1] )
           
        
    @lock_for_acess
    def get_candlestick(self,pos):
        '''returns the candlestick in the position pos. pos=0 is the first and pos=self.size-1 is the last'''
        
        v = Candlestick( self.df.iloc[ pos ] ,self.df.index[pos] )
           
        return v

    @lock_for_acess
    def inconsistency_check(self):
        '''returns None if data is OK or int indicating the first data wrong encountered from the end to the beginning '''
        bad_i_data = None
        for i in range(len(self.df)-1,0,-1) :                          # from the end to the begining
            preceding_close_time = self.df.iloc[i-1]["close_time"]     
            actual_close_time = self.df.index[i]
            if preceding_close_time +1  != actual_close_time:        
                bad_i_data = i -1 
                break
        
        return bad_i_data    




            



