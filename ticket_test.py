import hashlib
import time
import queue
from queue import *
import threading
import sqlite3
import logging

class tickets(object):
  def __init__(self):

        self.__requestid=None
        self.ticketid=None;
        self.q=queue.Queue();
        
        self.q=Queue(maxsize=10)
        self.timer1=0
        self.timer2=0
  def queued_tickets(self,requestid):
       self.conn = sqlite3.connect('testings.db')
       self.__requestid = requestid;       
       hash = hashlib.sha256()
       
       if (self.timer1==5):
          time.sleep(1)
          self.timer1=0
          
       hash.update(((requestid)).encode('utf-8'))       
       self.ticketid= hash.hexdigest()[0:5]       

       self.conn.execute('''INSERT INTO IDS (Requestid,Ticketid)
                          VALUES (?,?)''', (requestid,self.ticketid));
       
       self.conn.close()
       self.q.put(self.ticketid)
       print(" ticket request in queue ")
       self.timer1+=1
       
       
  def get_ticket_id(self):    
    if (self.timer2==2):
      time.sleep(1)
      self.timer2=0

    print( self.q.get())
    print("ticket allocated")
    self.timer2+=1
   
       
def Main():
  
  ticketissued = tickets();  
  for num in range(0,1000):

   tr1=threading.Thread(target=ticketissued.queued_tickets, args=('t1'+str(num),))
   tr1.start()
   tr2=threading.Thread(target=ticketissued.get_ticket_id)
   tr2.start()
  
   tr1.join()
   tr2.join()
   

if __name__ == '__main__':
   Main()



      
     

