import ROOT
from array import array

class EventData:
    def __init__(self):
        self.runNumber_arr          = array('i', [0] )
        self.eventNumber_arr        = array('l', [0] )
            
    def SetBranchAddress(self,intree):
        intree.SetBranchAddress( 'run', self.runNumber_arr)
        intree.SetBranchAddress( 'event', self.eventNumber_arr)


    def setEvent(self):
        self.runNumber          = self.runNumber_arr        [0]         
        self.eventNumber        = self.eventNumber_arr      [0]
