import optparse
parser = optparse.OptionParser()
parser.add_option('-i', '--inFileName',           dest="infileName",         default=None, help="Run in loop mode")
parser.add_option('-o', '--outFileName',          dest="outfileName",        default=None, help="Run in loop mode")
parser.add_option('-n', '--nevents',              dest="nevents",           default=None, help="Run in loop mode")
o, a = parser.parse_args()

import ROOT
from array import array
ROOT.gROOT.SetBatch(True) 
ROOT.gROOT.ProcessLine('.L Loader.C+')


inFile = ROOT.TFile(o.infileName,"READ")

inFile.ls()
tree = inFile.Get("ggNtuplizer/EventTree")
#tree = inFile.Get("EventTree")
tree.Print("eleCali*")

#
# Input Data 
#
from eventData  import EventData
from jetInfo    import JetDataHandler
from leptonInfo import ElectronDataHandler

eventData = EventData()
eventData.SetBranchAddress(tree)


#
#  Load Jet info
#
jetDB = JetDataHandler()
jetDB.SetBranchAddress(tree)



#
#  Load Electron info
#
elecDB = ElectronDataHandler()
elecDB.SetBranchAddress(tree)


#
# Make output ntuple
# 
outFile    = ROOT.TFile(o.outfileName,"recreate")
nEventThisFile = tree.GetEntries()
print( "Number of input events: %s" % nEventThisFile )

iEvent = 0


#
# histograms
#
from eventHists import EventHists

hInc = EventHists("",outFile)
hZPt80 = EventHists("ZPt80_",outFile)

#hJetsAll     = JetHists("AllJets",     outFile)
#
#hJetsAll     = JetHists("AllJets",     outFile)
#hAK8JetsAll  = JetHists("AllAK8Jets",  outFile, doSubJets=True)
#hAK16JetsAll = JetHists("AllAK16Jets",  outFile, doSubJets=True)
#hOneJet      = JetHists("OneJet",      outFile)
#hTwoJet      = JetHists("TwoJet",      outFile)
#hThreeJet    = JetHists("ThreeJet",    outFile)
#hFourJet     = JetHists("FourJet",     outFile)

#hjetPt   = ROOT.TH1F("jetPt","jetPt",100,0,200)
#hnjet    = ROOT.TH1F("njet" ,"njet" ,10,-0.5,9.5)

heleIDMVA  = ROOT.TH1F("eleIDMVA" ,"eleIDMVA" ,100,-1.2,1.2)
hneleSel   = ROOT.TH1F("neleSel" ,"neleSel" ,5,-0.5,4.5)
hmee       = ROOT.TH1F("mee" ,"mee" ,100,0,150)


for entry in xrange( 0,nEventThisFile): # let's only run over the first 100 events for this example                                                         
    tree.GetEntry( entry )

    iEvent +=1
    
    if iEvent %10000 == 0:
        print "Processed .... ",iEvent,"Events"
    if o.nevents and (iEvent > int(o.nevents) and int(o.nevents) > 0):
        break

    eventData.setEvent()

    #
    # Print event details
    #
    #print "RunNumber",runNumber[0],
    #print "EventNumber",eventNumber[0]

    # 
    #  Print Elecs
    # 
    elecPassID = elecDB.getElec(ptCut=20, mvaCut = -0.75)
    for elec in elecPassID:
        heleIDMVA.Fill(elec.IDMVA)

    
    hneleSel.Fill(len(elecPassID))

    #
    #  Zee Selection 
    #
    if len(elecPassID) < 2: continue
    ZCand_vec = (elecPassID[0].vec+elecPassID[1].vec)
    mee_12 = ZCand_vec.M()
    if abs(mee_12 - 91) > 10:  continue
    hmee.Fill(mee_12)

    if len(elecPassID) > 2:
        continue 
        print "RunNumber",eventData.runNumber,
        print "EventNumber",eventData.eventNumber
        for elec in elecPassID:
            print "\telec (pt,eta,phi)",elec.vec.Pt(),elec.vec.Eta(),elec.vec.Phi()
         

    # 
    #  Get Ak4 Jets
    # 
    jets_ak4  = jetDB.getJets(ptCut=35,elecsOlap=elecPassID)

    # Recluster to make AK8 Jets
    #debug = len(jets_ak4)>1
    debug = False
    if debug:
        print "="*10,"New Event","="*10

    if debug: print "Cluster to make AK8"
    jets_ak8  = jetDB.clusterJets(inJets=jets_ak4,  radius=0.8, debug = debug)
    if debug: print "Cluster to make AK16"
    jets_ak16 = jetDB.clusterJets(inJets=jets_ak8,  radius=1.6, debug = debug)
    if debug: print "Cluster to make AK20"
    jets_ak20 = jetDB.clusterJets(inJets=jets_ak16, radius=2.0, debug = debug)
    if debug: print "Cluster to make AK32"
    jets_ak32 = jetDB.clusterJets(inJets=jets_ak20, radius=3.2, debug = debug)

    if debug:
        hInc.makeDisplay(jets_ak4, jets_ak8, jets_ak16, jets_ak20, jets_ak32, ZCand_vec, elecPassID[0].vec, elecPassID[1].vec)



    hInc.Fill(jets_ak4, jets_ak8, jets_ak16, jets_ak20, jets_ak32, ZCand_vec)



    if ZCand_vec.Pt() > 80:
        hZPt80.Fill(jets_ak4, jets_ak8, jets_ak16, jets_ak20, jets_ak32, ZCand_vec)        
        if hZPt80.nDisplays < 100:
            hZPt80.makeDisplay(jets_ak4, jets_ak8, jets_ak16, jets_ak20, jets_ak32, ZCand_vec, elecPassID[0].vec, elecPassID[1].vec)
    
        
    #
    # Leptons ect
    #



hInc    .Write(outFile)
hZPt80  .Write(outFile)
#hAK8JetsAll.Write(outFile)
#hAK16JetsAll.Write(outFile)
#hOneJet   .Write(outFile)
#hTwoJet   .Write(outFile)
#hThreeJet .Write(outFile)
#hFourJet  .Write(outFile)

heleIDMVA.Write()
hneleSel.Write()
hmee.Write()
