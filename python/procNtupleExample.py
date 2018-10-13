import optparse
parser = optparse.OptionParser()
parser.add_option('-i', '--inFileName',           dest="infileName",         default=None, help="Run in loop mode")
parser.add_option('-o', '--outFileName',          dest="outfileName",        default=None, help="Run in loop mode")
parser.add_option('-n', '--nevents',              dest="nevents",           default=None, help="Run in loop mode")
o, a = parser.parse_args()

import ROOT
from array import array

ROOT.gROOT.ProcessLine('.L Loader.C+')


inFile = ROOT.TFile(o.infileName,"READ")

inFile.ls()
tree = inFile.Get("ggNtuplizer/EventTree")
tree.Print("eleCali*")


runNumber = array('i', [0] )
eventNumber = array('l', [0] )

#
#  Load Jet info
#
jetEn  = ROOT.std.vector('float')()
jetPt  = ROOT.std.vector('float')()
jetEta = ROOT.std.vector('float')()
jetPhi = ROOT.std.vector('float')()

tree.SetBranchAddress( 'jetEn', jetEn)
tree.SetBranchAddress( 'jetPt', jetPt)
tree.SetBranchAddress( 'jetEta',jetEta)
tree.SetBranchAddress( 'jetPhi',jetPhi)


#
#  Load Electron info
#
eleCalibEn = ROOT.std.vector('float')()
eleCalibPt = ROOT.std.vector('float')()
eleEta     = ROOT.std.vector('float')()
elePhi     = ROOT.std.vector('float')()
eleIDMVA   = ROOT.std.vector('float')()
tree.SetBranchAddress( 'eleCalibEn', eleCalibEn)
tree.SetBranchAddress( 'eleCalibPt', eleCalibPt)
tree.SetBranchAddress( 'eleEta',eleEta)
tree.SetBranchAddress( 'elePhi',elePhi)
tree.SetBranchAddress( 'eleIDMVA',eleIDMVA)


tree.SetBranchAddress( 'run', runNumber)
tree.SetBranchAddress( 'event', eventNumber)

#
# Make output ntuple
# 
f    = ROOT.TFile(o.outfileName,"recreate")
nEventThisFile = tree.GetEntries()
print( "Number of input events: %s" % nEventThisFile )

iEvent = 0


#
# histograms
#
hjetPt   = ROOT.TH1F("jetPt","jetPt",100,0,200)
hnjet    = ROOT.TH1F("njet" ,"njet" ,10,-0.5,9.5)
hnjetRaw = ROOT.TH1F("njetRaw" ,"njetRaw" ,10,-0.5,9.5)

heleIDMVA  = ROOT.TH1F("eleIDMVA" ,"eleIDMVA" ,100,-1.2,1.2)
hneleSel   = ROOT.TH1F("neleSel" ,"neleSel" ,5,-0.5,4.5)
hmee   = ROOT.TH1F("mee" ,"mee" ,100,0,150)


for entry in xrange( 0,nEventThisFile): # let's only run over the first 100 events for this example                                                         
    tree.GetEntry( entry )

    iEvent +=1
    
    if iEvent %10000 == 0:
        print "Processed .... ",iEvent,"Events"
    if o.nevents and (iEvent > int(o.nevents)):
        break

    #
    # Print event details
    #
    #print "RunNumber",runNumber[0],
    #print "EventNumber",eventNumber[0]

    # 
    #  Print Elecs
    # 
    elecPassID = []
    for iElec in range(eleEta.size()):
        if eleIDMVA.at(iElec) < -0.75: continue
        if eleCalibPt.at(iElec) < 20:  continue

        thisVector = ROOT.TLorentzVector()
        thisVector.SetPtEtaPhiE(eleCalibPt .at(iElec),
                                eleEta     .at(iElec),
                                elePhi     .at(iElec),
                                eleCalibEn .at(iElec))
        elecPassID.append(thisVector)
        heleIDMVA.Fill(eleIDMVA.at(iElec))

        
    
    hneleSel.Fill(len(elecPassID))

    if len(elecPassID) < 2: continue

    mee_12 = (elecPassID[0]+elecPassID[1]).M()
    if abs(mee_12 - 91) > 10:  continue

    hmee.Fill(mee_12)

    if len(elecPassID) > 2:
        print "RunNumber",runNumber[0],
        print "EventNumber",eventNumber[0]
        for elec in elecPassID:
            print "\telec (pt,eta,phi)",elec.Pt(),elec.Eta(),elec.Phi()
         

    # 
    #  Print Jets
    # 
    jetPassID = []
    for iJet in range(jetPt.size()):
        thisVector = ROOT.TLorentzVector()
        thisVector.SetPtEtaPhiM(jetPt .at(iJet),
                                jetEta.at(iJet),
                                jetPhi.at(iJet),
                                jetEn .at(iJet))

        passOverlap = True
        for elec in elecPassID:
            if thisVector.DeltaR(elec) < 0.4: passOverlap= False

        if not passOverlap:
            continue

        jetPassID.append(thisVector)
        #print "\tjet (pt,eta,phi)",thisVector.Pt(),thisVector.Eta(),thisVector.Phi()        
        hjetPt.Fill(thisVector.Pt())

    hnjet.Fill(len(jetPassID))
    hnjetRaw.Fill(jetPt.size())
    
        
    #
    # Leptons ect
    #

hjetPt.Write()
hnjet.Write()
hnjetRaw.Write()
heleIDMVA.Write()
hneleSel.Write()
hmee.Write()
