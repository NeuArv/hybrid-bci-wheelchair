#!/usr/bin/env python3
"""Run a small demo for the Hybrid BCI wheelchair scaffold"""
import numpy as np
from src.hybrid_bci.core import preprocess_eeg, extract_features, classify, generate_command

def main():
    raw = np.zeros(128)  # placeholder EEG buffer
    pre = preprocess_eeg(raw)
    feats = extract_features(pre)
    label, conf = classify(feats)
    cmd = generate_command(label)
    print('label=', label, 'conf=', conf, 'cmd=', cmd)

if __name__ == '__main__':
    main()
