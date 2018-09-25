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
tree = inFile.Get("EventTree")
tree.Print("jet*")


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
    print "RunNumber",runNumber[0],
    print "EventNumber",eventNumber[0]

    # 
    #  Print Jets
    # 
    for iJet in range(jetPt.size()):
        thisVector = ROOT.TLorentzVector()
        thisVector.SetPtEtaPhiM(jetPt .at(iJet),
                                jetEta.at(iJet),
                                jetPhi.at(iJet),
                                jetEn .at(iJet))

        print "\tjet (pt,eta,phi)",thisVector.Pt(),thisVector.Eta(),thisVector.Phi()        
        hjetPt.Fill(thisVector.Pt())
    hnjet.Fill(jetPt.size())
    
        
    #
    # Leptons ect
    #

hjetPt.Write()
hnjet.Write()
