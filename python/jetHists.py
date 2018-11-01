import ROOT
from array import array


class JetHists:

    def __init__(self,name, outFile, doSubJets = False):
        
        self.name = name
        self.doSubJets = doSubJets
        self.thisDir = outFile.mkdir(self.name)
        self.pt    = self.makeHist("pt","pt;P_{T} [GeV];Entries",  100,0,500)
        self.pt_m    = self.makeHist("pt_m","pt_m;P_{T} [GeV];Entries",  100,0,200)
        self.E     = self.makeHist("E","E;E [GeV];Entries",  100,0,500)
        self.eta   = self.makeHist("eta","eta;jet #eta;Entries",100,-3,3)
        self.phi   = self.makeHist("phi","phi;jet #phi;Entries",100,-3.2,3.2)
        self.mass  = self.makeHist("mass","mass;jet mass [GeV];Entries",100,-1,200)
        self.nJets = self.makeHist("nJets","nJets;jet Multiplicity",10,-0.5,9.5)
        self.nSubJets = self.makeHist("nSubJets","nSubJets;sub-jet Multiplicity",5,-0.5,4.5)
        self.nAk4Jets = self.makeHist("nAk4Jets","nAk4Jets;sub-ak4 jet Multiplicity",5,-0.5,4.5)
        self.dRClosest   = self.makeHist("dRClosest","dRClosest;jets;Entries",100,-0.1,6)
        self.dPhiClosest   = self.makeHist("dPhiClosest","dPhiClosest;jets;Entries",100,-3.2,3.2)
        self.dEtaClosest   = self.makeHist("dEtaClosest","dEtaClosest;jets;Entries",100,-5,5)


        self.sumJetPt  = self.makeHist("sumJetpt","sumJetpt;sum Jet P_{T} [GeV];Entries",  100,0,200)
        self.ZPt       = self.makeHist("Zpt","Zpt;Z P_{T} [GeV];Entries",  100,0,200)
        self.sumJetZPt = self.makeHist("sumJetZPt","sumJetZP;Jet + Z P_{T} [GeV];Entries",  100,0,200)
        self.dRsumJetZ    = self.makeHist("dRsumJetZ","dRsumJetZ;#Delta R^{sumJet,Z};Entries",  100,-0.1,6)
        self.dPhisumJetZ    = self.makeHist("dPhisumJetZ","dPhisumJetZ;#Delta #phi^{sumJet,Z};Entries",  100,-0.1,3.2)

        if self.doSubJets:
            self.pt_1    = self.makeHist("pt_1","pt_1;P_{T}^{1} [GeV];Entries",  100,0,500)
            self.pt_2    = self.makeHist("pt_2","pt_2;P_{T}^{2} [GeV];Entries",  100,0,500)
            self.Z_1     = self.makeHist("Z_1","Z_1;Z_1;Entries",  100,-0.1,1.1)
            self.Z_2     = self.makeHist("Z_2","Z_2;Z_2;Entries",  100,-0.1,1.1)

            self.dR         = self.makeHist("dR","dR;#Delta R^{1,2};Entries",  100,-0.1,6)
            self.dPhi       = self.makeHist("dPhi","dPhi;#Delta #phi^{1,2};Entries",  100,-0.1,6)


    def makeHist(self,name,title,bins,low,high):
        h = ROOT.TH1F(name,title,bins,low,high)
        h.SetDirectory(self.thisDir)
        return h

        
    def Fill(self,inJets, zVec = None):
        self.nJets.Fill(len(inJets))
        sumJetVec = None
        for jet in inJets:
            self.pt  .Fill(jet.vec.Pt())
            self.pt_m.Fill(jet.vec.Pt())
            self.eta .Fill(jet.vec.Eta())
            self.phi .Fill(jet.vec.Phi())
            self.mass.Fill(jet.vec.M())
            self.E   .Fill(jet.vec.E())
            if sumJetVec:
                sumJetVec = (sumJetVec + jet.vec)
            else:
                sumJetVec = jet.vec
            self.nSubJets.Fill(jet.nSubJets)
            self.nAk4Jets.Fill(jet.getNAk4Seeds())

            dRClosest = 100
            dPhiClosest = 100
            dEtaClosest = 100
            for jet_Other in inJets:
                if jet == jet_Other: continue
                thisDr = jet.vec.DeltaR(jet_Other.vec)
                if thisDr < dRClosest:
                    dRClosest = thisDr
                    dPhiClosest = jet.vec.DeltaPhi(jet_Other.vec)
                    dEtaClosest = jet.vec.Eta()-jet_Other.vec.Eta()
            if dRClosest < 10:
                self.dRClosest.Fill(dRClosest)
                self.dPhiClosest.Fill(dPhiClosest)
                self.dEtaClosest.Fill(dEtaClosest)

            if self.doSubJets:
                if jet.nSubJets > 1: 
        
                    subjet0 = jet.subJets[0]
                    subjet1 = jet.subJets[1]
        
                    self.dR.Fill(subjet0.vec.DeltaR(subjet1.vec))
                    self.dPhi.Fill(subjet0.vec.DeltaPhi(subjet1.vec))
        
                    self.pt_1.Fill(  subjet0.vec.Pt())
                    self.pt_2.Fill(  subjet1.vec.Pt())

                    self.Z_1.Fill(  subjet0.vec.E()/jet.vec.E())
                    self.Z_2.Fill(  subjet1.vec.E()/jet.vec.E())
        


        if zVec and sumJetVec:
            self.sumJetPt .Fill(sumJetVec.Pt())
            self.ZPt      .Fill(zVec.Pt())
            self.sumJetZPt.Fill((sumJetVec+zVec).Pt())
            self.dRsumJetZ.Fill(sumJetVec.DeltaR(zVec))
            self.dPhisumJetZ.Fill(abs(sumJetVec.DeltaPhi(zVec)))


    def Write(self,outFile):
        self.thisDir.cd()
        self.pt  .Write()
        self.pt_m  .Write()
        self.E   .Write()
        self.eta .Write()
        self.phi .Write()
        self.mass.Write()
        self.nJets.Write()
        self.nSubJets.Write()
        self.nAk4Jets.Write()
        self.dRClosest.Write()
        self.dPhiClosest.Write()
        self.dEtaClosest.Write()

        self.sumJetPt .Write()
        self.ZPt      .Write()
        self.sumJetZPt.Write()
        self.dRsumJetZ.Write()
        self.dPhisumJetZ.Write()

        if self.doSubJets:
            self.pt_1.Write()
            self.pt_2.Write()
            self.dR.Write()
            self.dPhi.Write()
            self.Z_1.Write()
            self.Z_2.Write()


        outFile.cd()
