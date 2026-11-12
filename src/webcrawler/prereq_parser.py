"""
I generated this helper script with Claude, parsing through the syntax tree of prequisite 
information was going to be a lot of grunt work for only a little payoff, plus I needed to move on with the project. 

Parse prerequisite text into AND-of-OR course groups plus leftover notes.

parse_prereqs(parts) -> (groups, notes)

groups: [[a, b], [c]] means (a OR b) AND c. Every group must be satisfied by at least one
        of its courses. "(A and B) or C" is expanded to [[A, C], [B, C]].
notes:  statements that are not course codes (permission, placement, "or equivalent", ...).

Reading rules for and/or (loosest to tightest):
  ;                            clause break
  ", and" / ", or" / ", either" / "and one of the following:"   (comma-prefixed = clause level)
  bare "and"
  bare "or"                    (so "A and B or C" is A and (B or C))
  "A or B and C"               is A or (B and C) when B, C share a department and A does not
  A/B, "22 or 24", A-B         tightest ("/" and shorthand numbers = OR, hyphen = AND)
Inside "one of the following: ..." every comma and ", or" is a plain OR list.
"""
import re

_NUM = r"\d{1,3}(?:\.\d{1,2})?"
# Department: capitalized, 2-5 letters (COSC, Math, Biol). Optional "-" or no space (HSE-101, PSYC1).
# Optional slash alternatives: MATH 22/24, COSC 70/70.01, BIOL/EEES 133
_CODE = re.compile(rf"\b((?:[A-Z][A-Za-z]{{1,4}}/)*[A-Z][A-Za-z]{{1,4}})\s*-?\s*({_NUM})((?:/{_NUM})*)(?!\d)")
# Bare number inheriting the previous department: "PSYC 1 or 6"
_BARE = re.compile(rf"\s*,?\s*(or|and)\s+({_NUM})(?!\d)", re.I)

# Words that look like a department when followed by a number ("Two 30-level", "AP Lang 4")
_STOP = {"OR", "AND", "TWO", "THREE", "FOUR", "FIVE", "FALL", "LANG", "LIT",
         "WEEK", "TERM", "YEAR", "PART", "LEVEL", "GRADE", "PLUS"}
# Words allowed to remain in a sentence once codes are removed ("one of the following")
_FILLER = {"and", "or", "of", "the", "following", "one", "two", "three", "plus",
           "either", "all", "any", "from", "a", "an", "only", "at", "least"}

_FORMERLY = re.compile(
    r"\(?\s*,?\s*\b(?:formerly|previously)\s+[A-Za-z]{2,5}\s*\d+(?:\.\d+)?\s*\)?", re.I)
_SPLIT = re.compile(r"(?<=\.)(?<!e\.g\.)\s+(?=[A-Z(\"'])|(?=Recommended Preparation)")
_SKIP = re.compile(r"recommended|co-?requisite|\bnot open\b|\bmay not\b|\bcannot\b", re.I)
_COUNT = re.compile(r"\b(?:two|three|four)\s+(?:out\s+)?of\b", re.I)  # "at least two of ..."
_PERM = re.compile(
    r"(?:[;,:]\s*)?(?:\b(?:or|and)\b,?\s*)?(?:with\s+)?(?:written\s+)?"
    r"(?:(?:the\s+)?(?:instructor|chair|department|faculty)'?s?\s+)?permissions?\b",
    re.I,
)

_MAX_CLAUSES = 64


# ---------------------------------------------------------------- course codes

def _fmt(dept, num):
    whole, _, frac = num.partition(".")
    return f"{dept} {int(whole)}" + (f".{frac}" if frac else "")


def _dept(code):
    return code.split()[0]


def _extract(text):
    """Return [(code, start, end, kind)] in order. kind: '' | 'slash' | 'short-or' | 'short-and'."""
    items = []
    for m in _CODE.finditer(text):
        depts = [d.upper() for d in m.group(1).split("/")]
        if depts[-1] in _STOP:
            continue
        nums = [m.group(2)] + list(filter(None, m.group(3).split("/")))
        for d, dept in enumerate(depts):
            for n, num in enumerate(nums):
                if d == 0 and n == 0:
                    items.append((_fmt(dept, num), m.start(), m.end(2), ""))
                else:                                             # MATH 22/24, BIOL/EEES 133
                    items.append((_fmt(dept, num), m.end(2), m.end(), "slash"))
        pos = m.end()
        while b := _BARE.match(text, pos):                        # PSYC 1 or 6
            items.append((_fmt(depts[-1], b.group(2)), b.start(2), b.end(2),
                          "short-" + b.group(1).lower()))
            pos = b.end()
    return items


def _has_extra(text):
    """True if text has meaningful words beyond course codes and connectives."""
    rest = _CODE.sub(lambda m: m.group(0) if m.group(1).split("/")[-1].upper() in _STOP else " ", text)
    return any(w.lower() not in _FILLER for w in re.findall(r"[A-Za-z']+", rest))


# ------------------------------------------------------------ and/or structure

def _gap(gap):
    """Describe the text between two course codes."""
    conns = re.findall(r"\b(and|or)\b", gap, re.I)
    return {
        "opens": gap.count("("), "closes": gap.count(")"),
        "conn": conns[-1].upper() if conns else None,
        "semi": ";" in gap,
        "comma": "," in gap,
        "comma_conn": bool(re.search(r",\s*\)?\s*(?:and|or)\b", gap, re.I)),
        "one_of": bool(re.search(r"\bone of\b", gap, re.I)),
        "either": bool(re.search(r"\beither\b", gap, re.I)),
        "slash": bool(re.fullmatch(r"\s*/\s*", gap)),
        "hyphen": bool(re.fullmatch(r"\s*[-\u2013]\s*", gap)),
    }


def _operators(head, items):
    """One [op, rank, bare, in_list] per gap. Higher rank binds tighter."""
    lead = head[:items[0][1]]
    depth = lead.count("(")
    in_list = bool(re.search(r"\bone of\b", lead, re.I))
    list_depth = 0
    gaps = [_gap(head[a[2]:b[1]]) for a, b in zip(items, items[1:])]
    ops = []
    for g, item in zip(gaps, items[1:]):
        kind = item[3]
        d = max(depth - g["closes"], 0)
        bare = False
        leaves_list = False
        if kind == "slash" or g["slash"]:
            op, rank = "OR", 6
        elif kind.startswith("short"):
            op, rank = kind[6:].upper(), 6
        elif g["hyphen"]:
            op, rank = "AND", 6
        elif g["semi"]:
            op, rank = g["conn"] or "AND", 1
            in_list = False
            if g["one_of"]:
                in_list, list_depth = True, d
        elif g["one_of"] or g["either"]:
            op, rank = g["conn"] or "AND", 2
            if g["one_of"]:
                in_list, list_depth = True, d
        elif g["comma_conn"]:
            op = g["conn"]
            rank = 4 if (in_list and op == "OR") else 2
            leaves_list = op == "AND"
        elif g["conn"]:
            op = g["conn"]
            rank, bare = (4 if op == "OR" else 3), True
            leaves_list = op == "AND"
        elif g["comma"]:
            op, rank = "COMMA", 0
        else:
            op, rank = "AND", 3
            leaves_list = True
        ops.append([op, rank, bare, in_list])
        if leaves_list and d <= list_depth:
            in_list = False
        depth = d + g["opens"]

    # plain commas: an OR inside "one of" lists, otherwise decided by what follows the run
    for k, o in enumerate(ops):
        if o[0] != "COMMA":
            continue
        if o[3]:
            o[0], o[1] = "OR", 4
            continue
        j = k + 1
        while j < len(ops) and ops[j][0] == "COMMA":
            j += 1
        if j < len(ops):
            g = gaps[j]
            if g["semi"] or g["one_of"] or g["either"]:
                op = "AND"
            elif g["comma_conn"]:
                op = g["conn"]                                     # "A, B, or C"
            elif g["conn"] and _dept(items[k][0]) == _dept(items[k + 1][0]):
                op = g["conn"]                                     # "Math 22, Math 24 or COSC 70"
            else:
                op = "AND"                                         # "MATH 13, PHYS 13, ENGS 20 or ..."
        else:
            m = re.match(r"\s*\)*\s*,\s*(and|or)\b", head[items[-1][2]:], re.I)
            op = m.group(1).upper() if m else "AND"
        o[0], o[1] = op, (4 if op == "OR" else 2)

    # "X or Y and Z": the AND binds tighter when Y, Z share a department and X does not
    for k in range(1, len(ops)):
        if ops[k][:3] == ["AND", 3, True] and ops[k - 1][0] == "OR" and ops[k - 1][2] \
                and not ops[k][3] \
                and _dept(items[k][0]) == _dept(items[k + 1][0]) != _dept(items[k - 1][0]) \
                and (k + 1 >= len(ops) or ops[k + 1][0] != "OR"):
            ops[k][1] = 5
    return ops


def _tree(head, items):
    """Precedence-climbing parse. Nodes are course codes or (op, [children])."""
    ops = _operators(head, items)
    gaps = [_gap(head[a[2]:b[1]]) for a, b in zip(items, items[1:])]
    tokens, depth = [], 0

    def opens(n):
        nonlocal depth
        tokens.extend(["("] * n)
        depth += n

    def closes(n):
        nonlocal depth
        n = min(n, depth)                                          # ignore stray ")"
        tokens.extend([")"] * n)
        depth -= n

    opens(head[:items[0][1]].count("("))
    tokens.append(items[0][0])
    for g, (op, rank, *_), item in zip(gaps, ops, items[1:]):
        closes(g["closes"])
        tokens.append((op, rank))
        opens(g["opens"])
        tokens.append(item[0])
    closes(head[items[-1][2]:].count(")"))

    pos = 0

    def operand():
        nonlocal pos
        tok = tokens[pos]
        pos += 1
        if tok == "(":
            node = expr(0)
            if pos < len(tokens) and tokens[pos] == ")":
                pos += 1
            return node
        return tok

    def expr(min_rank):
        nonlocal pos
        left = operand()
        while pos < len(tokens) and isinstance(tokens[pos], tuple) and tokens[pos][1] >= min_rank:
            op, rank = tokens[pos]
            pos += 1
            right = expr(rank + 1)
            kids = (left[1] if isinstance(left, tuple) and left[0] == op else [left]) + \
                   (right[1] if isinstance(right, tuple) and right[0] == op else [right])
            left = (op, kids)
        return left

    return expr(0)


def _cnf(node):
    """Expand a tree into AND-of-OR clauses: [[code, ...], ...]."""
    if isinstance(node, str):
        return [[node]]
    op, kids = node
    parts = [_cnf(k) for k in kids]
    if op == "AND":
        return [c for p in parts for c in p]
    out = [[]]
    for p in parts:
        out = [o + c for o in out for c in p]
    return out


def _simplify(clauses):
    """Drop repeated codes, duplicate clauses, and clauses implied by a shorter one."""
    sets = [frozenset(c) for c in clauses]
    out, seen = [], set()
    for c, s in zip(clauses, sets):
        if s in seen or any(o < s for o in sets):
            continue
        seen.add(s)
        out.append(list(dict.fromkeys(c)))
    return out


# ------------------------------------------------------------------ public API

def parse_prereqs(parts):
    """Parse a prerequisite string (or list of string fragments) into (groups, notes)."""
    text = parts if isinstance(parts, str) else " ".join(parts)
    text = _FORMERLY.sub("", re.sub(r"\s+", " ", text.replace("\xa0", " "))).strip()

    clauses, notes = [], []
    for sentence in filter(None, (s.strip() for s in _SPLIT.split(text))):
        if _SKIP.search(sentence) or _COUNT.search(sentence):
            notes.append(sentence.strip(" ;,:"))                  # not representable as groups
            continue
        head, tail = sentence, ""
        if m := _PERM.search(sentence):                           # "; or Instructor Permission ..."
            head, tail = sentence[:m.start()], sentence[m.start():]
        items = _extract(head)
        if not items:                                             # no codes: pure statement
            notes.append(sentence.strip(" ;,:"))
            continue
        if _has_extra(head):
            notes.append(head.strip(" ;,:"))
        if tail:
            notes.append(tail.strip(" ;,:"))
        expanded = _cnf(_tree(head, items))
        if len(expanded) > _MAX_CLAUSES:
            notes.append("Too complex to expand: " + head.strip(" ;,:"))
            continue
        clauses.extend(expanded)

    return _simplify(clauses), list(dict.fromkeys(n for n in notes if n))