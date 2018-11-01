import ROOT
from array import array
import json


from jetHists import JetHists

class jetMult:
    def __init__(self,name, outFile):    
        self.name = name
        self.ak4  = JetHists(self.name+"_ak4",  outFile)
        self.ak8  = JetHists(self.name+"_ak8",  outFile, doSubJets=True)
        self.ak16 = JetHists(self.name+"_ak16", outFile, doSubJets=True)
        self.ak20 = JetHists(self.name+"_ak20", outFile, doSubJets=True)
        self.ak32 = JetHists(self.name+"_ak32", outFile, doSubJets=True)

    def Fill(self,jets_ak4, jets_ak8, jets_ak16, jets_ak20, jets_ak32,  ZCand_vec):
        self.ak4    .Fill(jets_ak4,  ZCand_vec)
        self.ak8    .Fill(jets_ak8,  ZCand_vec)
        self.ak16   .Fill(jets_ak16, ZCand_vec)
        self.ak20   .Fill(jets_ak20, ZCand_vec)
        self.ak32   .Fill(jets_ak32, ZCand_vec)

    def Write(self,outFile):
        self.ak4  .Write(outFile)
        self.ak8  .Write(outFile)
        self.ak16 .Write(outFile)
        self.ak20 .Write(outFile)
        self.ak32 .Write(outFile)


class EventHists:

    def __init__(self,name, outFile):
        self.name = name
        self.nDisplays = 0

        self.haj      = jetMult(self.name+"aj",  outFile)
        self.h1j      = jetMult(self.name+"1j",  outFile)
        self.h2j      = jetMult(self.name+"2j",  outFile)
        self.h3j      = jetMult(self.name+"3j",  outFile)
        self.h4j      = jetMult(self.name+"4j",  outFile)

        # 
        # For Event Displays
        #
        self.eventDisplayData = {}
        self.eventDisplayData["jets_ak4"]  = {}
        self.eventDisplayData["jets_ak8"]  = {}
        self.eventDisplayData["jets_ak12"] = {}
        self.eventDisplayData["jets_ak16"] = {}
        self.eventDisplayData["jets_ak20"] = {}
        self.eventDisplayData["jets_ak32"] = {}
        self.eventDisplayData["ZVec"]      = {}
        self.eventDisplayData["ElecVec"]      = {}

        
    def Fill(self, jets_ak4, jets_ak8, jets_ak16, jets_ak20, jets_ak32, ZCand_vec):

        self.haj.Fill(jets_ak4, jets_ak8, jets_ak16,  jets_ak20,  jets_ak32,  ZCand_vec)

        if len(jets_ak4) == 1:
            self.h1j.Fill(jets_ak4, jets_ak8, jets_ak16,  jets_ak20,  jets_ak32,  ZCand_vec)

        elif len(jets_ak4) == 2:
            self.h2j.Fill(jets_ak4, jets_ak8, jets_ak16,  jets_ak20,  jets_ak32,  ZCand_vec)

    
        elif len(jets_ak4) == 3:
            self.h3j.Fill(jets_ak4, jets_ak8, jets_ak16,  jets_ak20,  jets_ak32,  ZCand_vec)
    
        elif len(jets_ak4) == 4:
            self.h4j.Fill(jets_ak4, jets_ak8, jets_ak16,  jets_ak20,  jets_ak32,  ZCand_vec)
    

    def makeDisplay(self, jets_ak4, jets_ak8, jets_ak16, jets_ak20,  jets_ak32, ZCand_vec, elecVec1, elecVec2):
        
        #print "Filling ",self.nDisplays
        

        self.eventDisplayData["jets_ak4"][int(self.nDisplays)] = []
        for ak4j in jets_ak4:
            #print "  Jet ak4",ak4j.vec.Eta(),ak4j.vec.Phi(),ak4j.vec.Pt()
            self.eventDisplayData["jets_ak4"][int(self.nDisplays)].append((ak4j.vec.Eta(),ak4j.vec.Phi(),ak4j.vec.Pt()))


        self.eventDisplayData["jets_ak8"][int(self.nDisplays)] = []
        for ak8j in jets_ak8:
            #print "  Jet ak8",ak8j.vec.Eta(),ak8j.vec.Phi(),ak8j.vec.Pt()
            self.eventDisplayData["jets_ak8"][int(self.nDisplays)].append((ak8j.vec.Eta(),ak8j.vec.Phi(),ak8j.vec.Pt()))


        self.eventDisplayData["jets_ak16"][int(self.nDisplays)] = []
        for ak16j in jets_ak16:
            #print "  Jet ak16",ak16j.vec.Eta(),ak16j.vec.Phi(),ak16j.vec.Pt()
            self.eventDisplayData["jets_ak16"][int(self.nDisplays)].append((ak16j.vec.Eta(),ak16j.vec.Phi(),ak16j.vec.Pt()))


        self.eventDisplayData["jets_ak20"][int(self.nDisplays)] = []
        for ak20j in jets_ak20:
            #print "  Jet ak20",ak20j.vec.Eta(),ak20j.vec.Phi(),ak20j.vec.Pt()
            self.eventDisplayData["jets_ak20"][int(self.nDisplays)].append((ak20j.vec.Eta(),ak20j.vec.Phi(),ak20j.vec.Pt()))


        self.eventDisplayData["jets_ak32"][int(self.nDisplays)] = []
        for ak32j in jets_ak32:
            #print "  Jet ak32",ak32j.vec.Eta(),ak32j.vec.Phi(),ak32j.vec.Pt()
            self.eventDisplayData["jets_ak32"][int(self.nDisplays)].append((ak32j.vec.Eta(),ak32j.vec.Phi(),ak32j.vec.Pt()))


        self.eventDisplayData["ZVec"][int(self.nDisplays)] = (ZCand_vec.Eta(),ZCand_vec.Phi(),ZCand_vec.Pt())
        self.eventDisplayData["ElecVec"][int(self.nDisplays)] = [(elecVec1.Eta(),elecVec1.Phi(),elecVec1.Pt()),
                                                                 (elecVec2.Eta(),elecVec2.Phi(),elecVec2.Pt()),
                                                                 ]
        self.nDisplays += 1

    def Write(self,outFile):

        self.haj.Write(outFile)
        self.h1j.Write(outFile)
        self.h2j.Write(outFile)
        self.h3j.Write(outFile)
        self.h4j.Write(outFile)

        with open('Events'+self.name+'.txt', 'w') as outfile:  
            json.dump(self.eventDisplayData, outfile)    
