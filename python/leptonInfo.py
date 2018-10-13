import ROOT
from array import array


class elecData:

    def __init__(self,pt,eta,phi,En,IDMVA):
        self.pt = pt
        self.eta = eta
        self.phi = phi
        self.En = En
        self.IDMVA = IDMVA

        self.vec = ROOT.TLorentzVector()
        self.vec.SetPtEtaPhiE(pt,eta,phi,En)



#
# Separate File ? 
#
class ElectronDataHandler:

    def __init__(self):
        
        self.eleCalibEn = ROOT.std.vector('float')()
        self.eleCalibPt = ROOT.std.vector('float')()
        self.eleEta     = ROOT.std.vector('float')()
        self.elePhi     = ROOT.std.vector('float')()
        self.eleIDMVA   = ROOT.std.vector('float')()


        
    def SetBranchAddress(self,intree):
        intree.SetBranchAddress( 'eleCalibEn', self.eleCalibEn)
        intree.SetBranchAddress( 'eleCalibPt', self.eleCalibPt)
        intree.SetBranchAddress( 'eleEta',self.eleEta)
        intree.SetBranchAddress( 'elePhi',self.elePhi)
        intree.SetBranchAddress( 'eleIDMVA',self.eleIDMVA)


    def getElec(self,ptCut=-1,mvaCut=-2):

        elecPassID = []
        for iElec in range(self.eleEta.size()):
            if self.eleCalibPt.at(iElec) < ptCut:  continue
            if self.eleIDMVA.at(iElec) < mvaCut: continue
            
            elecPassID.append(elecData(self.eleCalibPt .at(iElec),
                                       self.eleEta     .at(iElec),
                                       self.elePhi     .at(iElec),
                                       self.eleCalibEn .at(iElec),
                                       self.eleIDMVA   .at(iElec),
                                       )
                              )

        return elecPassID
