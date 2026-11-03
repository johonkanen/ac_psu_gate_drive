#!/usr/bin/env python3
"""Search the JLCPCB parts library for candidate parts (keyword search); prints code, stock, library
type (Basic/Extended), MPN, package and description. Used once to pick the codes of fab/jlc_bom.csv.

  python3 fab/jlc_search.py "SI8271" "ZLLS400TA" ...
"""
import json, sys, time, urllib.request

URL = "https://jlcpcb.com/api/overseas-pcb-order/v1/shoppingCart/smtGood/selectSmtComponentList"


def search(kw, n=15):
    req = urllib.request.Request(URL, data=json.dumps({"keyword": kw, "currentPage": 1, "pageSize": n}).encode(),
                                 headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
    for _ in range(3):
        try:
            d = json.load(urllib.request.urlopen(req, timeout=30))
            return (d.get("data") or {}).get("componentPageInfo", {}).get("list") or []
        except Exception:
            time.sleep(2)
    return []


if __name__ == "__main__":
    for kw in sys.argv[1:]:
        print(f"== {kw}")
        for c in sorted(search(kw), key=lambda c: -(c.get("stockCount") or 0)):
            print(f"  {c['componentCode']:10} {c.get('stockCount') or 0:>8} {c.get('componentLibraryType') or '-':9} "
                  f"{(c.get('componentModelEn') or '')[:30]:30} {(c.get('componentSpecificationEn') or '')[:12]:12} "
                  f"{(c.get('describe') or '')[:70]}")
        time.sleep(0.3)
