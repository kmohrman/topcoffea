'''
 selection.py

 This script contains several functions that implement the some event selection. 
 The functinos defined here can be used to define a selection, signal/control region, etc.
 The functions are called with (jagged)arrays as imputs plus some custom paramenters and return a boolean mask.

'''

import numpy as np

def passNJets(nJets, lim=2):
  return nJets >= lim

def passMETcut(met, metCut=40):
  return met >= metCut

# Datasets:
# SingleElec, SingleMuon
# DoubleElec, DoubleMuon, MuonEG
# Overlap removal at trigger level... singlelep, doublelep, triplelep

triggers = {
  'SingleMuonTriggers' : {'2016': ['IsoMu24', 'IsoMu27'],
                          '2017': ['IsoMu24', 'IsoMu27'],
                          '2018': ['IsoMu24', 'IsoMu27']},
  'SingleElecTriggers' : {'2016': ['Ele27_WPTight_Gsf'],
                          '2017': ['Ele32_WPTight_Gsf', 'Ele35_WPTight_Gsf'],
                          '2018': ['Ele32_WPTight_Gsf', 'Ele35_WPTight_Gsf']},
  'DoubleMuonTrig' : {'2016':['Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ'],
                      '2017':['Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ', 'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'],
                      '2018':['Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ', 'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8']},
  'DoubleElecTrig' : {'2016':['Ele23_Ele12_CaloIdL_TrackIdL_IsoVL', 'Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'],
                      '2017':['Ele23_Ele12_CaloIdL_TrackIdL_IsoVL', 'Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'],
                      '2018':['Ele23_Ele12_CaloIdL_TrackIdL_IsoVL', 'Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ']},
  'MuonEGTrig' : {'2016':['Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL', 'Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ', 'Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'],
                  '2017':['Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL', 'Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ', 'Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'],
                  '2018':['Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL', 'Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ', 'Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ']},
  'TripleElecTrig' : {'2016': ['Ele16_Ele12_Ele8_CaloIdL_TrackIdL'],
                      '2017': ['Ele16_Ele12_Ele8_CaloIdL_TrackIdL'],
                      '2018': ['Ele16_Ele12_Ele8_CaloIdL_TrackIdL']},
  'TripleMuonTrig' : {'2016': ['TripleMu_12_10_5'],
                      '2017': ['TripleMu_12_10_5'],
                      '2018': ['TripleMu_12_10_5']},
  'DoubleMuonElecTrig' : {'2016': ['DiMu9_Ele9_CaloIdL_TrackIdL'],
                          '2017': ['DiMu9_Ele9_CaloIdL_TrackIdL_DZ'],
                          '2018': ['DiMu9_Ele9_CaloIdL_TrackIdL_DZ']},
  'DoubleElecMuonTrig' : {'2016': ['Mu8_DiEle12_CaloIdL_TrackIdL'],
                          '2017': ['Mu8_DiEle12_CaloIdL_TrackIdL'],
                          '2018': ['Mu8_DiEle12_CaloIdL_TrackIdL']},
}

triggersForFinalState = {
  'ee' : {
      'MC': {'2016': triggers['SingleElecTriggers']['2016']+triggers['DoubleElecTrig']['2016'],
             '2017': triggers['SingleElecTriggers']['2017']+triggers['DoubleElecTrig']['2017'],
             '2018': triggers['SingleElecTriggers']['2018']+triggers['DoubleElecTrig']['2018']},
      'EGamma': {'2016': triggers['SingleElecTriggers']['2016']+triggers['DoubleElecTrig']['2016'],
                 '2017': triggers['SingleElecTriggers']['2017']+triggers['DoubleElecTrig']['2017'],
                 '2018': triggers['SingleElecTriggers']['2018']+triggers['DoubleElecTrig']['2018']},
  },
  'em' : {
      'MC': {'2016': triggers['SingleElecTriggers']['2016']+triggers['SingleMuonTriggers']['2016']+triggers['MuonEGTrig']['2016'],
             '2017': triggers['SingleElecTriggers']['2017']+triggers['SingleMuonTriggers']['2017']+triggers['MuonEGTrig']['2017'],
             '2018': triggers['SingleElecTriggers']['2018']+triggers['SingleMuonTriggers']['2018']+triggers['MuonEGTrig']['2018']},
      'EGamma'     : {'2016': triggers['SingleElecTriggers']['2016'],
                      '2017': triggers['SingleElecTriggers']['2017'],
                      '2018': triggers['SingleElecTriggers']['2018']},
      'MuonEG'     : {'2016': triggers['MuonEGTrig']['2016'],
                      '2017': triggers['MuonEGTrig']['2017'],
                      '2018': triggers['MuonEGTrig']['2018']},
      'SingleMuon' : {'2016': triggers['SingleElecTriggers']['2016'],
                      '2017': triggers['SingleElecTriggers']['2017'],
                      '2018': triggers['SingleElecTriggers']['2018']},
  },
  'mm' : {
      'MC': {'2016': triggers['SingleMuonTriggers']['2016']+triggers['DoubleMuonTrig']['2016'],
             '2017': triggers['SingleMuonTriggers']['2017']+triggers['DoubleMuonTrig']['2017'],
             '2018': triggers['SingleMuonTriggers']['2018']+triggers['DoubleMuonTrig']['2018']},
      'DoubleMuon' : {'2016': triggers['DoubleMuonTrig']['2016'],
                      '2017': triggers['DoubleMuonTrig']['2017'],
                      '2018': triggers['DoubleMuonTrig']['2018']},
      'SingleMuon' : {'2016': triggers['SingleMuonTriggers']['2016'],
                      '2017': triggers['SingleMuonTriggers']['2017'],
                      '2018': triggers['SingleMuonTriggers']['2018']},
  },
  'eee' : {
      'MC': {'2016': triggers['SingleElecTriggers']['2016']+triggers['DoubleElecTrig']['2016']+triggers['TripleElecTrig']['2016'],
             '2017': triggers['SingleElecTriggers']['2017']+triggers['DoubleElecTrig']['2017']+triggers['TripleElecTrig']['2017'],
             '2018': triggers['SingleElecTriggers']['2018']+triggers['DoubleElecTrig']['2018']+triggers['TripleElecTrig']['2018']},
      'EGamma' : {'2016': triggers['SingleElecTriggers']['2016']+triggers['DoubleElecTrig']['2016']+triggers['TripleElecTrig']['2016'],
                  '2017': triggers['SingleElecTriggers']['2017']+triggers['DoubleElecTrig']['2017']+triggers['TripleElecTrig']['2017'],
                  '2018': triggers['SingleElecTriggers']['2018']+triggers['DoubleElecTrig']['2018']+triggers['TripleElecTrig']['2018']},
  },
  'mmm' : {
      'MC': {'2016': triggers['SingleMuonTriggers']['2016']+triggers['DoubleMuonTrig']['2016']+triggers['TripleMuonTrig']['2016'],
             '2017': triggers['SingleMuonTriggers']['2017']+triggers['DoubleMuonTrig']['2017']+triggers['TripleMuonTrig']['2017'],
             '2018': triggers['SingleMuonTriggers']['2018']+triggers['DoubleMuonTrig']['2018']+triggers['TripleMuonTrig']['2018']},
      'DoubleMuon' : {'2016': triggers['DoubleMuonTrig']['2016']+triggers['TripleMuonTrig']['2016'],
                      '2017': triggers['DoubleMuonTrig']['2017']+triggers['TripleMuonTrig']['2017'],
                      '2018': triggers['DoubleMuonTrig']['2018']+triggers['TripleMuonTrig']['2018']},
      'SingleMuon' : {'2016': triggers['SingleMuonTriggers']['2016'],
                      '2017': triggers['SingleMuonTriggers']['2017'],
                      '2018': triggers['SingleMuonTriggers']['2018']},
  },
  'eem' : {
      'MC':{'2016': triggers['SingleMuonTriggers']['2016']+triggers['SingleElecTriggers']['2016']+triggers['DoubleElecTrig']['2016']+triggers['MuonEGTrig']['2016']+triggers['DoubleElecMuonTrig']['2016'],
            '2017': triggers['SingleMuonTriggers']['2017']+triggers['SingleElecTriggers']['2017']+triggers['DoubleElecTrig']['2017']+triggers['MuonEGTrig']['2017']+triggers['DoubleElecMuonTrig']['2017'],
            '2018': triggers['SingleMuonTriggers']['2018']+triggers['SingleElecTriggers']['2018']+triggers['DoubleElecTrig']['2018']+triggers['MuonEGTrig']['2018']+triggers['DoubleElecMuonTrig']['2018']},
      'MuonEG' : {'2016': triggers['MuonEGTrig']['2016']+triggers['DoubleElecMuonTrig']['2016'],
                  '2017': triggers['MuonEGTrig']['2017']+triggers['DoubleElecMuonTrig']['2017'],
                  '2018': triggers['MuonEGTrig']['2018']+triggers['DoubleElecMuonTrig']['2018']},
      'EGamma' : {'2016': triggers['SingleElecTriggers']['2016']+triggers['DoubleElecTrig']['2016'],
                  '2017': triggers['SingleElecTriggers']['2017']+triggers['DoubleElecTrig']['2017'],
                  '2018': triggers['SingleElecTriggers']['2018']+triggers['DoubleElecTrig']['2018']},
      'SingleMuon' : {'2016': triggers['SingleMuonTriggers']['2016'],
                      '2017': triggers['SingleMuonTriggers']['2017'],
                      '2018': triggers['SingleMuonTriggers']['2018']},
  },
  'mme' : {
      'MC':{'2016': triggers['SingleMuonTriggers']['2016']+triggers['SingleElecTriggers']['2016']+triggers['DoubleMuonTrig']['2016']+triggers['MuonEGTrig']['2016']+triggers['DoubleMuonElecTrig']['2016'],
            '2017': triggers['SingleMuonTriggers']['2017']+triggers['SingleElecTriggers']['2017']+triggers['DoubleMuonTrig']['2017']+triggers['MuonEGTrig']['2017']+triggers['DoubleMuonElecTrig']['2017'],
            '2018': triggers['SingleMuonTriggers']['2018']+triggers['SingleElecTriggers']['2018']+triggers['DoubleMuonTrig']['2018']+triggers['MuonEGTrig']['2018']+triggers['DoubleMuonElecTrig']['2018']},
      'MuonEG' : {'2016': triggers['DoubleMuonTrig']['2016']+triggers['DoubleMuonElecTrig']['2016'],
                  '2017': triggers['DoubleMuonTrig']['2017']+triggers['DoubleMuonElecTrig']['2017'],
                  '2018': triggers['DoubleMuonTrig']['2018']+triggers['DoubleMuonElecTrig']['2018']},
      'EGamma' : {'2016': triggers['SingleElecTriggers']['2016'],
                  '2017': triggers['SingleElecTriggers']['2017'],
                  '2018': triggers['SingleElecTriggers']['2018']},
      'DoubleMuon' : {'2016': triggers['DoubleMuonTrig']['2016'],
                      '2017': triggers['DoubleMuonTrig']['2017'],
                      '2018': triggers['DoubleMuonTrig']['2018']},
      'SingleMuon' : {'2016': triggers['SingleElecTriggers']['2016'],
                    '2017': triggers['SingleElecTriggers']['2017'],
                    '2018': triggers['SingleElecTriggers']['2018']},
  },
  'eeee' : {
      'MC': {'2016': triggers['SingleElecTriggers']['2016']+triggers['DoubleElecTrig']['2016']+triggers['TripleElecTrig']['2016'],
             '2017': triggers['SingleElecTriggers']['2017']+triggers['DoubleElecTrig']['2017']+triggers['TripleElecTrig']['2017'],
             '2018': triggers['SingleElecTriggers']['2018']+triggers['DoubleElecTrig']['2018']+triggers['TripleElecTrig']['2018']},
      'EGamma' : {'2016': triggers['SingleElecTriggers']['2016']+triggers['DoubleElecTrig']['2016']+triggers['TripleElecTrig']['2016'],
                  '2017': triggers['SingleElecTriggers']['2017']+triggers['DoubleElecTrig']['2017']+triggers['TripleElecTrig']['2017'],
                  '2018': triggers['SingleElecTriggers']['2018']+triggers['DoubleElecTrig']['2018']+triggers['TripleElecTrig']['2018']},
  },
  'mmmm' : {
      'MC':{'2016': triggers['SingleMuonTriggers']['2016']+triggers['DoubleMuonTrig']['2016']+triggers['TripleMuonTrig']['2016'],
            '2017': triggers['SingleMuonTriggers']['2017']+triggers['DoubleMuonTrig']['2017']+triggers['TripleMuonTrig']['2017'],
            '2018': triggers['SingleMuonTriggers']['2018']+triggers['DoubleMuonTrig']['2018']+triggers['TripleMuonTrig']['2018']},
      'DoubleMuon' : {'2016': triggers['DoubleMuonTrig']['2016']+triggers['TripleMuonTrig']['2016'],
                      '2017': triggers['DoubleMuonTrig']['2017']+triggers['TripleMuonTrig']['2017'],
                      '2018': triggers['DoubleMuonTrig']['2018']+triggers['TripleMuonTrig']['2018']},
      'SingleMuon' : {'2016': triggers['SingleMuonTriggers']['2016'],
                      '2017': triggers['SingleMuonTriggers']['2017'],
                      '2018': triggers['SingleMuonTriggers']['2018']},
  },
  'eeem' : {
      'MC': {'2016': triggers['TripleElecTrig']['2016']+triggers['SingleMuonTriggers']['2016']+triggers['SingleElecTriggers']['2016']+triggers['DoubleElecTrig']['2016']+triggers['MuonEGTrig']['2016']+triggers['DoubleElecMuonTrig']['2016'],
             '2017': triggers['TripleElecTrig']['2017']+triggers['SingleMuonTriggers']['2017']+triggers['SingleElecTriggers']['2017']+triggers['DoubleElecTrig']['2017']+triggers['MuonEGTrig']['2017']+triggers['DoubleElecMuonTrig']['2017'],
             '2018': triggers['TripleElecTrig']['2018']+triggers['SingleMuonTriggers']['2018']+triggers['SingleElecTriggers']['2018']+triggers['DoubleElecTrig']['2018']+triggers['MuonEGTrig']['2018']+triggers['DoubleElecMuonTrig']['2018']},
      'MuonEG' : {'2016': triggers['DoubleMuonTrig']['2016']+triggers['DoubleMuonElecTrig']['2016'],
                  '2017': triggers['DoubleMuonTrig']['2017']+triggers['DoubleMuonElecTrig']['2017'],
                  '2018': triggers['DoubleMuonTrig']['2018']+triggers['DoubleMuonElecTrig']['2018']},
      'EGamma' : {'2016': triggers['SingleElecTriggers']['2016']+triggers['DoubleElecTrig']['2016']+triggers['TripleElecTrig']['2016'],
                  '2017': triggers['SingleElecTriggers']['2017']+triggers['DoubleElecTrig']['2017']+triggers['TripleElecTrig']['2017'],
                  '2018': triggers['SingleElecTriggers']['2018']+triggers['DoubleElecTrig']['2018']+triggers['TripleElecTrig']['2018']},
      'SingleMuon' : {'2016': triggers['SingleMuonTriggers']['2016'],
                      '2017': triggers['SingleMuonTriggers']['2017'],
                      '2018': triggers['SingleMuonTriggers']['2018']},
  },
  'eemm' : {
      'MC': {'2016':  triggers['SingleMuonTriggers']['2016']+triggers['SingleElecTriggers']['2016']+triggers['DoubleElecTrig']['2016']+triggers['DoubleMuonTrig']['2016']+triggers['MuonEGTrig']['2016']+triggers['DoubleElecMuonTrig']['2016']+triggers['DoubleMuonElecTrig']['2016'],
             '2017':  triggers['SingleMuonTriggers']['2017']+triggers['SingleElecTriggers']['2017']+triggers['DoubleElecTrig']['2017']+triggers['DoubleMuonTrig']['2017']+triggers['MuonEGTrig']['2017']+triggers['DoubleElecMuonTrig']['2017']+triggers['DoubleMuonElecTrig']['2017'],
             '2018':  triggers['SingleMuonTriggers']['2018']+triggers['SingleElecTriggers']['2018']+triggers['DoubleElecTrig']['2018']+triggers['DoubleMuonTrig']['2018']+triggers['MuonEGTrig']['2018']+triggers['DoubleElecMuonTrig']['2018']+triggers['DoubleMuonElecTrig']['2018']},
      'MuonEG' : {'2016': triggers['DoubleMuonTrig']['2016']+triggers['DoubleMuonElecTrig']['2016']+triggers['MuonEGTrig']['2016'],
                  '2017': triggers['DoubleMuonTrig']['2017']+triggers['DoubleMuonElecTrig']['2017']+triggers['MuonEGTrig']['2017'],
                  '2018': triggers['DoubleMuonTrig']['2018']+triggers['DoubleMuonElecTrig']['2018']+triggers['MuonEGTrig']['2018']},
      'EGamma' : {'2016': triggers['SingleElecTriggers']['2016']+triggers['DoubleElecTrig']['2016']+triggers['TripleElecTrig']['2016'],
                  '2017': triggers['SingleElecTriggers']['2017']+triggers['DoubleElecTrig']['2017']+triggers['TripleElecTrig']['2017'],
                  '2018': triggers['SingleElecTriggers']['2018']+triggers['DoubleElecTrig']['2018']+triggers['TripleElecTrig']['2018']},
      'SingleMuon' : {'2016': triggers['SingleMuonTriggers']['2016'],
                      '2017': triggers['SingleMuonTriggers']['2017'],
                      '2018': triggers['SingleMuonTriggers']['2018']},
      'DoubleMuon' : {'2016': triggers['DoubleMuonTrig']['2016'],
                      '2017': triggers['DoubleMuonTrig']['2017'],
                      '2018': triggers['DoubleMuonTrig']['2018']},
  },
  'mmme' : {
      'MC': {'2016': triggers['TripleMuonTrig']['2016']+triggers['SingleMuonTriggers']['2016']+triggers['SingleElecTriggers']['2016']+triggers['DoubleMuonTrig']['2016']+triggers['MuonEGTrig']['2016']+triggers['DoubleMuonElecTrig']['2016'],
             '2017': triggers['TripleMuonTrig']['2017']+triggers['SingleMuonTriggers']['2017']+triggers['SingleElecTriggers']['2017']+triggers['DoubleMuonTrig']['2017']+triggers['MuonEGTrig']['2017']+triggers['DoubleMuonElecTrig']['2017'],
             '2018': triggers['TripleMuonTrig']['2018']+triggers['SingleMuonTriggers']['2018']+triggers['SingleElecTriggers']['2018']+triggers['DoubleMuonTrig']['2018']+triggers['MuonEGTrig']['2018']+triggers['DoubleMuonElecTrig']['2018']},
      'MuonEG' : {'2016': triggers['DoubleMuonTrig']['2016']+triggers['DoubleMuonElecTrig']['2016'],
                  '2017': triggers['DoubleMuonTrig']['2017']+triggers['DoubleMuonElecTrig']['2017'],
                  '2018': triggers['DoubleMuonTrig']['2018']+triggers['DoubleMuonElecTrig']['2018']},
      'EGamma' : {'2016': triggers['SingleElecTriggers']['2016']+triggers['DoubleElecTrig']['2016']+triggers['TripleElecTrig']['2016'],
                  '2017': triggers['SingleElecTriggers']['2017']+triggers['DoubleElecTrig']['2017']+triggers['TripleElecTrig']['2017'],
                  '2018': triggers['SingleElecTriggers']['2018']+triggers['DoubleElecTrig']['2018']+triggers['TripleElecTrig']['2018']},
      'SingleMuon' : {'2016': triggers['SingleMuonTriggers']['2016'],
                      '2017': triggers['SingleMuonTriggers']['2017'],
                      '2018': triggers['SingleMuonTriggers']['2018']},
  }
}

triggersNotForFinalState = {
  'ee' : {'EGamma' : [],},
  'em' : {
      'MuonEG'     : [],
      'EGamma'     : {'2016': triggers['MuonEGTrig']['2016'],
                      '2017': triggers['MuonEGTrig']['2017'],
                      '2018': triggers['MuonEGTrig']['2018']},
      'SingleMuon' : {'2016': triggers['MuonEGTrig']['2016'],
                      '2017': triggers['MuonEGTrig']['2017'],
                      '2018': triggers['MuonEGTrig']['2018']},
  },
  'mm' : {
      'DoubleMuon' : [],
      'SingleMuon' : {'2016': triggers['DoubleMuonTrig']['2016'],
                      '2017': triggers['DoubleMuonTrig']['2017'],
                      '2018': triggers['DoubleMuonTrig']['2018']},
  },
  'eee' : { 'EGamma' : [],},
  'mmm' : {
      'DoubleMuon' : [],
      'SingleMuon' : {'2016': triggers['DoubleMuonTrig']['2016']+triggers['TripleMuonTrig']['2016'],
                      '2017': triggers['DoubleMuonTrig']['2017']+triggers['TripleMuonTrig']['2017'],
                      '2018': triggers['DoubleMuonTrig']['2018']+triggers['TripleMuonTrig']['2018']},
  },
  'eem' : {
      'MuonEG' : [], 
      'EGamma' : {'2016': triggers['MuonEGTrig']['2016']+triggers['DoubleElecMuonTrig']['2016'],
                  '2017': triggers['MuonEGTrig']['2017']+triggers['DoubleElecMuonTrig']['2017'],
                  '2018': triggers['MuonEGTrig']['2018']+triggers['DoubleElecMuonTrig']['2018']},
      'SingleMuon' :  {'2016': triggers['SingleElecTriggers']['2016']+triggers['DoubleMuonTrig']['2016']+triggers['MuonEGTrig']['2016']+triggers['DoubleElecMuonTrig']['2016'],
                       '2017': triggers['SingleElecTriggers']['2017']+triggers['DoubleMuonTrig']['2017']+triggers['MuonEGTrig']['2017']+triggers['DoubleElecMuonTrig']['2017'],
                       '2018': triggers['SingleElecTriggers']['2018']+triggers['DoubleMuonTrig']['2018']+triggers['MuonEGTrig']['2018']+triggers['DoubleElecMuonTrig']['2018']},
  },
  'mme' : {
      'MuonEG' : [],
      'EGamma' : {'2016': triggers['MuonEGTrig']['2016']+triggers['DoubleElecMuonTrig']['2016'],
                  '2017': triggers['MuonEGTrig']['2017']+triggers['DoubleElecMuonTrig']['2017'],
                  '2018': triggers['MuonEGTrig']['2018']+triggers['DoubleElecMuonTrig']['2018']},
      'DoubleMuon' : {'2016': triggers['SingleElecTriggers']['2016']+triggers['MuonEGTrig']['2016']+triggers['DoubleElecMuonTrig']['2016'],
                      '2017': triggers['SingleElecTriggers']['2017']+triggers['MuonEGTrig']['2017']+triggers['DoubleElecMuonTrig']['2017'],
                      '2018': triggers['SingleElecTriggers']['2018']+triggers['MuonEGTrig']['2018']+triggers['DoubleElecMuonTrig']['2018']},
      'SingleMuon' : {'2016': triggers['SingleElecTriggers']['2016']+triggers['DoubleMuonTrig']['2016']+triggers['MuonEGTrig']['2016']+triggers['DoubleElecMuonTrig']['2016'],
                      '2017': triggers['SingleElecTriggers']['2017']+triggers['DoubleMuonTrig']['2017']+triggers['MuonEGTrig']['2017']+triggers['DoubleElecMuonTrig']['2017'],
                      '2018': triggers['SingleElecTriggers']['2018']+triggers['DoubleMuonTrig']['2018']+triggers['MuonEGTrig']['2018']+triggers['DoubleElecMuonTrig']['2018']},
  },
  'eeee' : { 'EGamma' : [],},
  'mmmm' : {
      'DoubleMuon' : [],
      'SingleMuon' : {'2016': triggers['DoubleMuonTrig']['2016']+triggers['TripleMuonTrig']['2016'],
                      '2017': triggers['DoubleMuonTrig']['2017']+triggers['TripleMuonTrig']['2017'],
                      '2018': triggers['DoubleMuonTrig']['2018']+triggers['TripleMuonTrig']['2018']},
  },
  'eeem' : {
      'MuonEG' : [], 
      'EGamma' : {'2016': triggers['MuonEGTrig']['2016']+triggers['DoubleElecMuonTrig']['2016'],
                  '2017': triggers['MuonEGTrig']['2017']+triggers['DoubleElecMuonTrig']['2017'],
                  '2018': triggers['MuonEGTrig']['2018']+triggers['DoubleElecMuonTrig']['2018']},
      'SingleMuon' : {'2016':  triggers['SingleMuonTriggers']['2016']+triggers['SingleElecTriggers']['2016']+triggers['DoubleElecTrig']['2016']+triggers['MuonEGTrig']['2016']+triggers['DoubleElecMuonTrig']['2016']+triggers['DoubleMuonElecTrig']['2016'],
                      '2017':  triggers['SingleMuonTriggers']['2017']+triggers['SingleElecTriggers']['2017']+triggers['DoubleElecTrig']['2017']+triggers['MuonEGTrig']['2017']+triggers['DoubleElecMuonTrig']['2017']+triggers['DoubleMuonElecTrig']['2017'],
                      '2018':  triggers['SingleMuonTriggers']['2018']+triggers['SingleElecTriggers']['2018']+triggers['DoubleElecTrig']['2018']+triggers['MuonEGTrig']['2018']+triggers['DoubleElecMuonTrig']['2018']+triggers['DoubleMuonElecTrig']['2018']},
  },
  'eemm' : {
      'MuonEG' : [], 
      'EGamma' : {'2016': triggers['MuonEGTrig']['2016']+triggers['DoubleElecMuonTrig']['2016']+triggers['DoubleMuonElecTrig']['2016'],
                  '2017': triggers['MuonEGTrig']['2017']+triggers['DoubleElecMuonTrig']['2017']+triggers['DoubleMuonElecTrig']['2017'],
                  '2018': triggers['MuonEGTrig']['2018']+triggers['DoubleElecMuonTrig']['2018']+triggers['DoubleMuonElecTrig']['2018']},
      'SingleMuon' : {'2016':  triggers['SingleMuonTriggers']['2016']+triggers['SingleElecTriggers']['2016']+triggers['DoubleElecTrig']['2016']+triggers['DoubleMuonTrig']['2016']+triggers['MuonEGTrig']['2016']+triggers['DoubleElecMuonTrig']['2016']+triggers['DoubleMuonElecTrig']['2016'],
                      '2017':  triggers['SingleMuonTriggers']['2017']+triggers['SingleElecTriggers']['2017']+triggers['DoubleElecTrig']['2017']+triggers['DoubleMuonTrig']['2017']+triggers['MuonEGTrig']['2017']+triggers['DoubleElecMuonTrig']['2017']+triggers['DoubleMuonElecTrig']['2017'],
                      '2018':  triggers['SingleMuonTriggers']['2018']+triggers['SingleElecTriggers']['2018']+triggers['DoubleElecTrig']['2018']+triggers['DoubleMuonTrig']['2018']+triggers['MuonEGTrig']['2018']+triggers['DoubleElecMuonTrig']['2018']+triggers['DoubleMuonElecTrig']['2018']},
  },
  'mmme' : {
      'MuonEG' : [],
      'EGamma' : {'2016': triggers['MuonEGTrig']['2016']+triggers['DoubleElecMuonTrig']['2016'],
                  '2017': triggers['MuonEGTrig']['2017']+triggers['DoubleElecMuonTrig']['2017'],
                  '2018': triggers['MuonEGTrig']['2018']+triggers['DoubleElecMuonTrig']['2018']},
      'DoubleMuon' : {'2016': triggers['MuonEGTrig']['2016']+triggers['DoubleElecMuonTrig']['2016']+triggers['SingleElecTriggers']['2016'],
                      '2017': triggers['MuonEGTrig']['2017']+triggers['DoubleElecMuonTrig']['2017']+triggers['SingleElecTriggers']['2017'],
                      '2018': triggers['MuonEGTrig']['2018']+triggers['DoubleElecMuonTrig']['2018']+triggers['SingleElecTriggers']['2018']},
      'SingleMuon' : {'2016': triggers['MuonEGTrig']['2016']+triggers['DoubleElecMuonTrig']['2016']+triggers['SingleElecTriggers']['2016']+triggers['DoubleMuonTrig']['2016']+triggers['TripleMuonTrig']['2016'],
                      '2017': triggers['MuonEGTrig']['2017']+triggers['DoubleElecMuonTrig']['2017']+triggers['SingleElecTriggers']['2017']+triggers['DoubleMuonTrig']['2017']+triggers['TripleMuonTrig']['2017'],
                      '2018': triggers['MuonEGTrig']['2018']+triggers['DoubleElecMuonTrig']['2018']+triggers['SingleElecTriggers']['2018']+triggers['DoubleMuonTrig']['2018']+triggers['TripleMuonTrig']['2018']},
  }
}

def passTrigger(df, cat, year, isData=False, dataName=''):
  tpass = np.zeros_like(np.array(df.MET.pt), dtype=np.bool)
  df = df.HLT
  if not isData: 
    paths = triggersForFinalState[cat]['MC'][year.__str__()]
    for path in paths:
      try:
        tpass = tpass | df[path]
      except ValueError:
        print("Warning! Trigger not in data. Skipping...")
        print(path)
      
  else:
    passTriggers    = triggersForFinalState[cat][dataName][date.__str__()] if dataName in triggersForFinalState[cat].keys() else []
    notPassTriggers = triggersNotForFinalState[cat][dataName][date.__str__()] if dataName in triggersNotForFinalState[cat].keys() else []
    for path in passTriggers: tpass = tpass| df[path]
    for path in notPassTriggers: tpass = (tpass)&(df[path]==0)
  return tpass

def triggerFor4l(df, nMuon, nElec, isData, dataName=''):
  is4lmask = ((nElec+nMuon)>=4)
  is4l0m = (is4lmask)&(nMuon==0)
  is4l1m = (is4lmask)&(nMuon==1)
  is4l2m = (is4lmask)&(nMuon==2)
  is4l3m = (is4lmask)&(nMuon==3)
  is4l4m = (is4lmask)&(nMuon>=4)
  trig4l0m = passTrigger(df, 'eeee', isData, dataName)
  trig4l1m = passTrigger(df, 'eeem', isData, dataName)
  trig4l2m = passTrigger(df, 'eemm', isData, dataName)
  trig4l3m = passTrigger(df, 'mmme', isData, dataName)
  trig4l4m = passTrigger(df, 'mmmm', isData, dataName)
  trigMask = ( ( (is4l0m)&(trig4l0m) )|( (is4l1m)&(trig4l1m) )|( (is4l2m)&(trig4l2m) )|( (is4l3m)&(trig4l3m) )|( (is4l4m)&(trig4l4m) ) )
  return trigMask

##################################################################################
### Fake rates

import uproot
from coffea import hist, lookup_tools
import os, sys
from topcoffea.modules.paths import topcoffea_path
import awkward as ak

extFakeRates = lookup_tools.extractor()
basepathFromTTH = 'data/fromTTH/fakerate/'

# Electron reco
#histoName = ''
#for leptype in ['el', 'mu']:
#  for year in [2016, 2017, 2018]:
#    hname = 'FR_mva090_mu_data_comb' if leptype == 'mu' else 'FR_mva090_el_data_comb_NC'
#    extFakeRates.add_weight_sets( ["fr_%s_%i %s %s"%(leptype, year, hname, topcoffea_path(basepathFromTTH+'fr_%i.root'%year) )] ) # pt, abs(eta)


#extFakeRates.finalize()
#FRevaluatior = extFakeRates.make_evaluator()
