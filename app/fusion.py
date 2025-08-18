def fuse(phish_prob: float = None, spoof_prob: float = None, meta_risk: float = 0.0):
    """
    phish_prob: probability email is phishing (None if not provided)
    spoof_prob: probability audio is spoof (None if not provided)
    meta_risk: small additive bump for bad signals (e.g., blacklisted domain) in [0,0.3]
    Strategy:
      - average available channels
      - add meta_risk
      - clamp [0,1]
    """
    parts = []
    if phish_prob is not None: parts.append(phish_prob)
    if spoof_prob is not None: parts.append(spoof_prob)
    base = sum(parts)/len(parts) if parts else 0.0
    score = max(0.0, min(1.0, base + meta_risk))
    label = int(score >= 0.5)
    return {'risk_score': score, 'label': label}
