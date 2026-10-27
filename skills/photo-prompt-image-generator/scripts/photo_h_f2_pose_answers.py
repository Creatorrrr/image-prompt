"""Recognize source-bound pose and bilateral arm witnesses."""
import re

def _sentence_ranges(text):
    start = 0
    for m in re.finditer(r"[.!?。！？\n]+", text):
        end = m.end()
        if text[start:end].strip():
            left, right = start, end
            while left < right and text[left].isspace():
                left += 1
            while right > left and text[right - 1].isspace():
                right -= 1
            if left < right:
                yield left, right
        start = end
    if start < len(text):
        left, right = start, len(text)
        while left < right and text[left].isspace():
            left += 1
        while right > left and text[right - 1].isspace():
            right -= 1
        if left < right:
            yield left, right


_MULTI_OWNER = re.compile(
    r"\b(?:two|three|several|both)\s+(?:people|persons|women|men|subjects|figures)\b|"
    r"\b(?:another|second|different)\s+(?:person|woman|man|subject|figure)\b|"
    r"(?:두|세|여러)\s*(?:사람|명|여성|인물|피사체)|"
    r"다른\s*(?:사람|여성|남성|인물|피사체)", re.I | re.U)
_NAMED_MULTI_OWNER = re.compile(
    r"\b(?!The\b|One\b|This\b|That\b|When\b|While\b|After\b|Before\b|Then\b)"
    r"[A-Z][a-z]{2,}\b[\s\S]{0,64}\b(?:and|while|whereas|but|&)\b"
    r"[\s\S]{0,64}\b[A-Z][a-z]{2,}\b")
_MIXED_GENDER_OWNERS = re.compile(
    r"\b(?:man|men|male|boy|he|him|his)\b[\s\S]{0,180}"
    r"\b(?:woman|women|female|girl|she|her|hers)\b|"
    r"\b(?:woman|women|female|girl|she|her|hers)\b[\s\S]{0,180}"
    r"\b(?:man|men|male|boy|he|him|his)\b|"
    r"(?:남성|남자|소년|그의)[\s\S]{0,180}(?:여성|여자|소녀|그녀)|"
    r"(?:여성|여자|소녀|그녀)[\s\S]{0,180}(?:남성|남자|소년|그의)", re.I | re.U)
_PAIR_UNCERTAIN_OR_QUOTED = re.compile(
    r"\b(?:maybe|perhaps|possibly|might|may|could|seems?|probably|if|whether)\b|"
    r"\b(?:not|never|without|no longer|isn't|aren't|wasn't|weren't|doesn't|don't)\b|"
    r"아마|듯(?:하다|한)?|수도\s*있|가능성|아니|않|못|없", re.I | re.U)
_PAIR_QUOTED = re.compile(r"[?？\"“”‘`]|(?<!\w)’|’(?!\w)", re.I | re.U)
_EN_ARM_PAIR = re.compile(
    r"(?P<first>\bone\s+arm\b)[\s\S]{0,240}?"
    r"(?P<other>\b(?:her|his|their)\s+other\s+arm\b)", re.I | re.U)
_KO_ARM_PAIR = re.compile(
    r"(?P<first>한\s*(?:쪽\s*)?팔(?:은|이|을|도|만)?)"
    r"[\s\S]{0,180}?"
    r"(?P<other>(?:다른\s*(?:쪽\s*)?팔|반대쪽\s*팔)(?:은|이|을|도|만)?)", re.U)


def same_owner_arm_pair(text, *, anchor_offset=None):
    """Find direct one/other limb evidence inside one sentence and source unit."""
    for start, end in _sentence_ranges(text):
        if anchor_offset is not None and not start <= anchor_offset < end:
            continue
        sentence = text[start:end]
        # Prefer a conservative abstention over combining limbs across owners,
        # contradictory possessives, negated or uncertain claims, and quotes.
        if (_MULTI_OWNER.search(sentence)
                or _NAMED_MULTI_OWNER.search(sentence)
                or _MIXED_GENDER_OWNERS.search(sentence)
                or _PAIR_QUOTED.search(sentence)):
            continue
        for pattern, language in ((_EN_ARM_PAIR, "en"), (_KO_ARM_PAIR, "ko")):
            match = pattern.search(sentence)
            if not match:
                continue
            context_start = max(0, match.start("first") - 40)
            context_end = min(len(sentence), match.end("other") + 40)
            if _PAIR_UNCERTAIN_OR_QUOTED.search(sentence[context_start:context_end]):
                continue
            pair_start = start + match.start("first")
            pair_end = start + match.end("other")
            return {
                "kind": "same_owner_one_other_arm_pair",
                "language": language,
                "first_arm": {"start": start + match.start("first"),
                              "end": start + match.end("first"),
                              "quote": match.group("first")},
                "other_arm": {"start": start + match.start("other"),
                              "end": start + match.end("other"),
                              "quote": match.group("other")},
                "source_span": {"start": pair_start, "end": pair_end,
                                "offset_unit": "unicode_code_points"},
                "source_quote": text[pair_start:pair_end],
            }
    return None


_ARM_ACTION_RX = {
    "raised": re.compile(
        r"\b(?:raise[ds]?|raising|lift(?:ed|s|ing)?)\b|\b(?:arm|arms)\b.{0,28}\b(?:up|overhead|above)\b|"
        r"팔.{0,20}(?:들|올리|위로)|(?:들어|올려).{0,20}팔", re.I | re.U),
    "hanging": re.compile(
        r"\bhang(?:s|ing)?\b|\b(?:arm|arms)\b.{0,28}\b(?:at her side|at his side|down|by her side|by his side)\b|"
        r"팔.{0,24}(?:늘어뜨리|내리|옆으로)|(?:늘어뜨리|내리).{0,20}팔", re.I | re.U),
    "crossed": re.compile(
        r"\bcross(?:ed|ing)?\b.{0,24}\barms?\b|\barms?\b.{0,24}\bcross(?:ed|ing)?\b|"
        r"팔.{0,20}(?:교차|포개)|(?:교차|포개).{0,20}팔", re.I | re.U),
}


def arm_action_guard(query_text, source_text):
    """Guard explicit bilateral actions; an open pose question stays unbound."""
    if not re.search(r"\barms?\b|팔", query_text, re.I | re.U):
        return {"status": "not_applicable", "requested": [], "source": []}
    requested = sorted(value for value, pattern in _ARM_ACTION_RX.items()
                       if pattern.search(query_text))
    source = sorted(value for value, pattern in _ARM_ACTION_RX.items()
                    if pattern.search(source_text))
    if not requested:
        return {"status": "open_unbound", "requested": [], "source": source}
    both_requested = bool(re.search(
        r"\b(?:both|two|each)\s+arms?\b|\b(?:arms?)\s+(?:on both sides)\b|양팔|양쪽\s*팔",
        query_text, re.I | re.U))
    if both_requested:
        bilateral_actions = {
            "raised": re.compile(
                r"\b(?:both|two)\s+arms?\b.{0,40}\b(?:raise[ds]?|raising|lift(?:ed|s|ing)?)\b|"
                r"\b(?:raise[ds]?|raising|lift(?:ed|s|ing)?)\b.{0,40}\b(?:both|two)\s+arms?\b|"
                r"양팔.{0,24}(?:들|올리)|(?:들어|올려).{0,24}양팔", re.I | re.U),
            "hanging": re.compile(
                r"\b(?:both|two)\s+arms?\b.{0,40}\bhang(?:s|ing)?\b|"
                r"\bhang(?:s|ing)?\b.{0,40}\b(?:both|two)\s+arms?\b|"
                r"양팔.{0,24}(?:늘어뜨리|내리)|(?:늘어뜨리|내려).{0,24}양팔", re.I | re.U),
            "crossed": re.compile(
                r"\b(?:both|two)\s+arms?\b.{0,40}\bcross(?:ed|ing)?\b|"
                r"\bcross(?:ed|ing)?\b.{0,40}\b(?:both|two)\s+arms?\b|"
                r"양팔.{0,24}(?:교차|포개)|(?:교차|포개).{0,24}양팔", re.I | re.U),
        }
        if not all(bilateral_actions[value].search(source_text) for value in requested):
            return {"status": "mismatch", "requested": requested, "source": source}
    if set(requested) <= set(source):
        return {"status": "supported", "requested": requested, "source": source}
    return {"status": "mismatch", "requested": requested, "source": source}

