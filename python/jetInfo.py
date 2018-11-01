import ROOT
from array import array


class jetData:

    def __init__(self,pt,eta,phi,En,nSubJets=1,subJets=[]):
        self.pt = pt
        self.eta = eta
        self.phi = phi
        self.En = En
        self.nSubJets  = nSubJets
        self.subJets   = subJets

        self.vec = ROOT.TLorentzVector()
        self.vec.SetPtEtaPhiE(pt,eta,phi,En)

    def copy(self):
        return jetData(self.pt,
                       self.eta,
                       self.phi,
                       self.En,
                       self.nSubJets,
                       self.subJets)
                       
    def Add(self,rhs):
        self.vec = (self.vec + rhs.vec)
        self.pt  = self.vec.Pt()
        self.eta = self.vec.Eta()
        self.phi = self.vec.Phi()
        self.en  = self.vec.E()
        self.subJets = [self.copy(),rhs.copy()]
        self.subJets.sort(key=lambda x: x.En, reverse=True)
        #self.nSubJets = (self.nSubJets + rhs.nSubJets)
        self.nSubJets += 1

    def getNAk4Seeds(self):
        
        if len(self.subJets) == 0:
            nAk4Seeds = 1
        else:
            nAk4Seeds = 0
            for s in self.subJets:
                nAk4Seeds += s.getNAk4Seeds()
            
        return nAk4Seeds

    def dump(self,newLine=True):
        return "pt/eta/phi/subjets/nak4Seeds "+str(self.pt)+" "+str(self.eta)+" "+str(self.phi)+" "+str(self.nSubJets)+" "+str(self.getNAk4Seeds())


#
# Separate File ? 
#
class JetDataHandler:

    def __init__(self):
        
        self.jetEn  = ROOT.std.vector('float')()
        self.jetPt  = ROOT.std.vector('float')()
        self.jetEta = ROOT.std.vector('float')()
        self.jetPhi = ROOT.std.vector('float')()

        
        
    def SetBranchAddress(self,intree):
        intree.SetBranchAddress( 'jetEn', self.jetEn)
        intree.SetBranchAddress( 'jetPt', self.jetPt)
        intree.SetBranchAddress( 'jetEta',self.jetEta)
        intree.SetBranchAddress( 'jetPhi',self.jetPhi)


    def getJets(self,ptCut=-1, elecsOlap=[]):

        jetSel = []
        for iJet in range(self.jetEta.size()):
            if self.jetPt.at(iJet) < ptCut:  continue
            
            thisJet = jetData(self.jetPt .at(iJet),
                              self.jetEta.at(iJet),
                              self.jetPhi.at(iJet),
                              self.jetEn .at(iJet),
                              )

            passOverlap = True
            for elec in elecsOlap:
                if thisJet.vec.DeltaR(elec.vec) < 0.4: passOverlap= False

            if not passOverlap:
                continue

            jetSel.append(thisJet)

        return jetSel


    def clusterJets(self,inJets,radius,debug=False):

        #debug = (len(inJets) > 1)
        #debug = False

        if debug:
            print "="*10,"In clusterJets","="*10

        inJetsCopy = list(inJets)
        
        # Sort based on PT
        inJets.sort(key=lambda x: x.pt, reverse=True)

        jetsAK8 = []

        if debug:
            print "inJets Before"
            nJets = len(inJets)
            for iJ in range(0,nJets):
                print "Have Jet",inJets[iJ].dump()

        
        while len(inJetsCopy):
            if debug:
                print "len(inJets)",len(inJets)
                print "len(inJetsCopy)",len(inJetsCopy)
            thisJetSeedRaw = inJetsCopy.pop(0)
            thisJetSeed = thisJetSeedRaw.copy()
            thisJetSeed.nSubJets = 1

            if debug:
                print "\tPopped Jet",thisJetSeed.dump()
            

            clustedJet = self.clusterSeed(thisJetSeed,inJetsCopy,radius,debug)
            if debug: print "Final Jet",clustedJet.dump()
            jetsAK8.append(clustedJet)                


        # Sort output jets based on PT
        jetsAK8.sort(key=lambda x: x.pt, reverse=True)

        if debug:
            print "inJets After"
            nJets = len(inJets)
            for iJ in range(0,nJets):
                print "Have Jet",inJets[iJ].dump()



        return jetsAK8

    def clusterSeed(self,jetSeed,jetList,radius,debug=False):
        nJets = len(jetList)
        for iJ in range(0,nJets):
            
            if debug: print "\t\tThis Jet",jetList[iJ].dump()
            
            thisDr = jetSeed.vec.DeltaR(jetList[iJ].vec)
            if debug: print thisDr
        
            if thisDr < radius:
                deltaJet = jetList.pop(iJ)
                jetSeed.Add(deltaJet)
                if debug: print "CLUSTERED Jet",jetSeed.dump()
                
                return self.clusterSeed(jetSeed,jetList,debug)

        return jetSeed
            


#        
#





#        jetSel = []
#        for iJet in range(self.jetEta.size()):
#            if self.jetPt.at(iJet) < ptCut:  continue
#            
#            thisJet = jetData(self.jetPt .at(iJet),
#                              self.jetEta.at(iJet),
#                              self.jetPhi.at(iJet),
#                              self.jetEn .at(iJet),
#                              )
#
#            passOverlap = True
#            for elec in elecsOlap:
#                if thisJet.vec.DeltaR(elec.vec) < 0.4: passOverlap= False
#
#            if not passOverlap:
#                continue
#
#            jetSel.append(thisJet)
#
#        return jetSel
