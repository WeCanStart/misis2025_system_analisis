import json
from math import isclose

def main(LVinput, LVoutput, rules, T):
    tol = 1e-9

    def parse_lv(json_obj):
        if isinstance(json_obj, str):
            data = json.loads(json_obj)
        else:
            data = json_obj
        if isinstance(data, dict):
            for v in data.values():
                if isinstance(v, list):
                    terms = v
                    break
            else:
                terms = []
        elif isinstance(data, list):
            terms = data
        else:
            terms = []
        norm = {}
        for term in terms:
            tid = term.get('id')
            pts = term.get('points', [])
            pts2 = [(float(p[0]), float(p[1])) for p in pts]
            pts2.sort(key=lambda x: x[0])
            norm[tid] = pts2
        return norm

    def eval_piecewise(pts, x):
        if not pts:
            return 0.0
        x = float(x)
        if x <= pts[0][0]:
            return float(pts[0][1])
        if x >= pts[-1][0]:
            return float(pts[-1][1])
        for (x1,y1),(x2,y2) in zip(pts, pts[1:]):
            if x1 <= x <= x2:
                if isclose(x2, x1):
                    return float(y2)
                t = (x - x1) / (x2 - x1)
                return float(y1 + (y2 - y1) * t)
        return 0.0

    def parse_rules_obj(rules_obj):
        if isinstance(rules_obj, str):
            obj = json.loads(rules_obj)
        else:
            obj = rules_obj
        rules = []
        if isinstance(obj, dict):
            for k,v in obj.items():
                if isinstance(k, str) and ',' in k:
                    for subk in [s.strip() for s in k.split(',') if s.strip()]:
                        rules.append((subk, v))
                else:
                    rules.append((k, v))
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, (list,tuple)) and len(item) >= 2:
                    rules.append((item[0], item[1]))
                elif isinstance(item, dict):
                    if 'if' in item and 'then' in item:
                        rules.append((item['if'], item['then']))
                    elif 'input' in item and 'output' in item:
                        rules.append((item['input'], item['output']))
                    elif 'from' in item and 'to' in item:
                        rules.append((item['from'], item['to']))
                    else:
                        keys = list(item.keys())
                        if len(keys) >= 2:
                            rules.append((item[keys[0]], item[keys[1]]))
        return [(str(a), str(b)) for a,b in rules]

    def compute_intersection(x1,y1,x2,y2, alpha):
        if isclose(y2, y1):
            return None
        t = (alpha - y1) / (y2 - y1)
        if t < -1e-12 or t > 1+1e-12:
            return None
        return x1 + t * (x2 - x1)

    def clip_function_preserve_plateau(points, alpha):
        if not points:
            return []
        alpha = float(alpha)
        nodes = []
        n = len(points)
        for i in range(n-1):
            x1,y1 = points[i]
            x2,y2 = points[i+1]
            y1c = min(y1, alpha)
            nodes.append((float(x1), float(y1c)))
            prod = (y1 - alpha) * (y2 - alpha)
            if prod < -tol:
                xi = compute_intersection(x1,y1,x2,y2, alpha)
                if xi is not None:
                    nodes.append((float(xi), float(alpha)))
        xlast, ylast = points[-1]
        nodes.append((float(xlast), float(min(ylast, alpha))))
        nodes.sort(key=lambda p: p[0])
        cleaned = []
        for x,y in nodes:
            if cleaned and isclose(cleaned[-1][0], x, abs_tol=1e-9):
                cleaned[-1] = (cleaned[-1][0], max(cleaned[-1][1], y))
            else:
                cleaned.append((x,y))
        compressed = []
        i = 0
        m = len(cleaned)
        while i < m:
            x_i, y_i = cleaned[i]
            if isclose(y_i, alpha, abs_tol=1e-9):
                j = i
                while j+1 < m and isclose(cleaned[j+1][1], alpha, abs_tol=1e-9):
                    j += 1
                left_x = cleaned[i][0]
                right_x = cleaned[j][0]
                compressed.append((left_x, alpha))
                if not isclose(right_x, left_x, abs_tol=1e-9):
                    compressed.append((right_x, alpha))
                i = j + 1
            else:
                compressed.append((x_i, y_i))
                i += 1
        final = []
        for p in compressed:
            if final and isclose(final[-1][0], p[0], abs_tol=1e-12) and isclose(final[-1][1], p[1], abs_tol=1e-12):
                continue
            final.append(p)
        return final

    LVin = parse_lv(LVinput)
    LVout = parse_lv(LVoutput)
    rules_pairs = parse_rules_obj(rules)
    input_deg = {}
    for name, pts in LVin.items():
        deg = float(eval_piecewise(pts, T))
        input_deg[name] = deg
    out_alpha = {}
    for a,b in rules_pairs:
        deg = input_deg.get(a, 0.0)
        if b not in out_alpha or deg > out_alpha[b]:
            out_alpha[b] = float(deg)
    for outname in LVout.keys():
        out_alpha.setdefault(outname, 0.0)
    clipped_map = {}
    for outname, pts in LVout.items():
        alpha = out_alpha.get(outname, 0.0)
        if alpha <= tol:
            clipped_map[outname] = []
        else:
            clipped = clip_function_preserve_plateau(pts, alpha)
            clipped_map[outname] = clipped
            clipped_r = [(round(x,6), round(y,6)) for x,y in clipped]
    all_y = []
    for pts in clipped_map.values():
        for x,y in pts:
            all_y.append(y)
    max_y = max(all_y) if all_y else 0.0
    if max_y <= tol:
        mids_all = []
        for pts in LVout.values():
            if pts:
                mids_all.append((pts[0][0] + pts[-1][0]) / 2.0)
        fallback = float(sum(mids_all) / len(mids_all)) if mids_all else 0.0
        return fallback
    raw_intervals = []
    for name, pts in clipped_map.items():
        if not pts:
            continue
        i = 0
        m = len(pts)
        while i < m:
            x_i, y_i = pts[i]
            if isclose(y_i, max_y, abs_tol=1e-7):
                j = i
                while j+1 < m and isclose(pts[j+1][1], max_y, abs_tol=1e-7):
                    j += 1
                l = float(pts[i][0])
                r = float(pts[j][0])
                raw_intervals.append((l, r, name))
                i = j + 1
            else:
                i += 1
    raw_int_log = [ (round(l,6), round(r,6), n) for l,r,n in raw_intervals ]
    intervals = []
    raw_sorted = sorted([(l,r) for l,r,n in raw_intervals], key=lambda p: p[0])
    for l,r in raw_sorted:
        if not intervals:
            intervals.append([l,r])
        else:
            if l <= intervals[-1][1] + 1e-9:
                intervals[-1][1] = max(intervals[-1][1], r)
            else:
                intervals.append([l,r])
    intervals = [(float(a), float(b)) for a,b in intervals]
    L = sum(max(0.0, r - l) for l,r in intervals)
    if L <= tol:
        pts_x = []
        for l,r in intervals:
            pts_x.append((l + r) / 2.0)
        if not pts_x:
            xs_at_max = []
            for pts in clipped_map.values():
                for x,y in pts:
                    if isclose(y, max_y, abs_tol=1e-7):
                        xs_at_max.append(x)
            if not xs_at_max:
                return 0.0
            res = float(sum(xs_at_max) / len(xs_at_max))
            return res
        res = float(sum(pts_x) / len(pts_x))
        return res
    s = 0.0
    for l,r in intervals:
        s += (r*r - l*l)
    x_opt = 0.5 * s / L
    return float(x_opt)
