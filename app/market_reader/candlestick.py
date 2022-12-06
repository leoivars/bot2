
import datetime
class Candlestick:
    ''' store data of a candle stick and perform basic operations with this data
        
    
    '''
    
    def __init__(self,df=None,open_time=None): 

        if df is None:
            self.open_time=0
            self.open=0
            self.high=0
            self.low=0
            self.close=0
            self.volume=0
            self.close_time=0
            self.closed = 0
        else:
            self.open_time=open_time
            self.open=df.get('open')
            self.high=df.get('high')
            self.low=df.get('low')
            self.close=df.get('close')
            self.volume=df.get('volume')
            self.close_time=df.get('close_time')
            self.closed = df.get('closed')

    def sign(self):
        ''' 1 = on bullish candlestik
           -1 = bearich candlestick
        '''
        if self.close>self.open:
            return 1
        else: 
            return -1    
       
    def body(self):
        ''' body size of the candlestick '''
        return abs(self.close-self.open)    

    def wick_upper(self):
        '''size of upper wick'''
        if self.open<=self.close:
            return self.high-self.close
        else:
            return self.high-self.open

    def wick_lower(self):
        '''size of lower wick'''
        if self.open<=self.close:
            return self.open-self.low
        else:
            return self.close-self.low

    def range(self):
        '''high - low of candlestick'''
        return self.high - self.low 

    def percent_parts(self):
        '''
        returns a tuple expressing wick_upper body and wick_lower in percentages.
        100% is the range of the candle
        if range = 0 then return (0,0,0)
        '''
        total = self.range()
        if total == 0:
            return 0,0,0

        percent_wick_upper  = round( self.wick_upper() / total * 100 ,2)
        percent_body        = round( self.body() / total * 100, 2 )
        percent_wick_lower  = round( self.wick_lower() / total * 100 ,2)

        return percent_wick_upper,percent_body,percent_wick_lower

    def __str__(self):
        return f'candlestick O {self.open} H {self.high} L {self.low} C {self.close} V {self.volume}'
    
    def __repr__(self):
        return self.__str__()    
        
    def print(self):
        print( '------------------------------------' )
        print( 'open_time' , datetime.datetime.fromtimestamp(self.open_time/1000 ).strftime('%Y-%m-%d %H:%M:%S'))
        print( 'open' , self.open )
        print( 'high', self.high )
        print( 'low' , self.low )
        print( 'close' , self.close )
        print( 'volume' , self.volume )
        print( 'close_time' ,datetime.datetime.fromtimestamp(self.close_time/1000 ).strftime('%Y-%m-%d %H:%M:%S')    )
        print( '------------------------------------' )
