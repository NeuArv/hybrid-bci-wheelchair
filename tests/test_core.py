from src.hybrid_bci.core import preprocess_eeg, extract_features, classify, generate_command

def test_pipeline():
    raw = [0]*128
    pre = preprocess_eeg(raw)
    feats = extract_features(pre)
    label, conf = classify(feats)
    cmd = generate_command(label)
    assert isinstance(pre, dict)
    assert isinstance(feats, dict)
    assert isinstance(label, str)
    assert isinstance(cmd, dict)
