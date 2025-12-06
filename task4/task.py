import json

def main(json_str: str, T: float) -> str:
    data = json.loads(json_str)
    x = T
    res = {}
    for category in data.values():
        for fn in category:
            pts = sorted(fn.get("points", []), key=lambda p: p[0])
            if not pts:
                val = None
            else:
                if x <= pts[0][0]:
                    val = float(pts[0][1])
                elif x >= pts[-1][0]:
                    val = float(pts[-1][1])
                else:
                    val = None
                    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                        if x1 <= x <= x2:
                            x1 = float(x1); x2 = float(x2)
                            y1 = float(y1); y2 = float(y2)
                            if x2 == x1:
                                val = y2
                            else:
                                t = (x - x1) / (x2 - x1)
                                val = y1 + (y2 - y1) * t
                            break
            res[fn.get("id")] = val
    return json.dumps(res, ensure_ascii=False)

if __name__ == '__main__':
    print(main('''
{
    "температура": [
        {
            "id": "холодно",
            "points": [
                [0,1],
                [18,1],
                [22,0],
                [50,0]
            ]
        },
        {
            "id": "комфортно",
            "points": [
                [18,0],
                [22,1],
                [24,1],
                [26,0]
            ]
        },
        {
            "id": "жарко",
            "points": [
                [0,0],
                [24,0],
                [26,1],
                [50,1]
            ]
        }
    ]
}''', 25))
