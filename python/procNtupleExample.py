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
f    = ROOT.TFile(o.outfileName,"recreate")
nEventThisFile = tree.GetEntries()
print( "Number of input events: %s" % nEventThisFile )

iEvent = 0


#
# histograms
#
hjetPt   = ROOT.TH1F("jetPt","jetPt",100,0,200)
hnjet    = ROOT.TH1F("njet" ,"njet" ,10,-0.5,9.5)

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
    mee_12 = (elecPassID[0].vec+elecPassID[1].vec).M()
    if abs(mee_12 - 91) > 10:  continue
    hmee.Fill(mee_12)

    if len(elecPassID) > 2:
        print "RunNumber",eventData.runNumber,
        print "EventNumber",eventData.eventNumber
        for elec in elecPassID:
            print "\telec (pt,eta,phi)",elec.vec.Pt(),elec.vec.Eta(),elec.vec.Phi()
         

    # 
    #  Print Jets
    # 
    jetPassID = jetDB.getJets(ptCut=35,elecsOlap=elecPassID)

    for jet in jetPassID:
        hjetPt.Fill(jet.vec.Pt())

    hnjet.Fill(len(jetPassID))
    
        
    #
    # Leptons ect
    #

hjetPt.Write()
hnjet.Write()
heleIDMVA.Write()
hneleSel.Write()
hmee.Write()
