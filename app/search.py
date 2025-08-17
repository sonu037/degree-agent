from typing import List, Dict, Any
import math

def text_match_score(query: str, text: str) -> float:
    if not query:
        return 0.5
    q = query.lower().split()
    t = text.lower()
    hits = sum(1 for w in q if w in t)
    return hits / max(len(q), 1)

def affordability_boost(tuition_type: str, total_fees: float) -> float:
    if tuition_type == "tuition_free":
        return 1.0
    if tuition_type == "low_cost":
        return 0.6
    try:
        if total_fees is not None:
            return max(0.1, min(0.5, 0.5 - (total_fees / 50000.0)))
    except:
        pass
    return 0.1

def accreditation_boost(accr: Dict[str, Any]) -> float:
    body = (accr or {}).get("body") or ""
    if not body:
        return 0.0
    prestigious = {"DEAC","ABET","SACSCOC","AACSB","EQUIS","AMBA","NAAC","UGC"}
    return 0.6 if body in prestigious else 0.3

def modality_boost(modality: str) -> float:
    return 0.4 if (modality or '').lower() == "online" else 0.1

def freshness_boost(last_checked: str) -> float:
    return 0.1

def score_program(p: Dict[str, Any], query: str) -> float:
    text = " ".join([p.get("title",""), p.get("university",""), " ".join(p.get("discipline",[]))])
    text_rel = text_match_score(query, text)
    tuition_type = p.get("tuition_type","standard")
    total = p.get("tuition_detail",{}).get("total_estimate", None)
    s = (
        0.50 * text_rel
        + 0.20 * affordability_boost(tuition_type, total)
        + 0.10 * accreditation_boost(p.get("accreditation"))
        + 0.10 * modality_boost(p.get("modality"))
        + 0.10 * freshness_boost(p.get("last_checked_utc"))
    )
    return round(s, 4)

def filter_program(p: Dict[str, Any], q: Dict[str, Any]) -> bool:
    if q.get("discipline"):
        if not any(d.lower() == q["discipline"].lower() for d in p.get("discipline", [])):
            return False
    if q.get("degree_level") and str(p.get("degree_level","")).lower() != q["degree_level"].lower():
        return False
    if q.get("tuition_type") and str(p.get("tuition_type","")).lower() != q["tuition_type"].lower():
        return False
    if q.get("country") and str(p.get("country","")).lower() != q["country"].lower():
        return False
    if q.get("modality") and str(p.get("modality","")).lower() != q["modality"].lower():
        return False
    if q.get("accreditation"):
        body = (p.get("accreditation") or {}).get("body","").lower()
        if q["accreditation"].lower() not in body:
            return False
    max_total = q.get("max_total_fees")
    if max_total is not None:
        total = (p.get("tuition_detail") or {}).get("total_estimate")
        if total is None or float(total) > float(max_total):
            return False
    return True
