import ROOT
from array import array


class jetData:

    def __init__(self,pt,eta,phi,En):
        self.pt = pt
        self.eta = eta
        self.phi = phi
        self.En = En

        self.vec = ROOT.TLorentzVector()
        self.vec.SetPtEtaPhiE(pt,eta,phi,En)



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
