import asyncio
import json
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import httpx
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


def normalize_ship_name(name: str) -> str:
    return (name or "").strip().upper()


def pad2(n: int) -> str:
    return str(n).zfill(2)


def to_ymd_dash(d: datetime) -> str:
    return f"{d.year}-{pad2(d.month)}-{pad2(d.day)}"


def to_ymd_compact(d: datetime) -> str:
    return f"{d.year}{pad2(d.month)}{pad2(d.day)}"


def parse_korean_like_datetime(s: str) -> Optional[datetime]:
    if not s:
        return None
    cleaned = str(s).replace("(", "").replace(")", "").strip()
    m = re.search(r"(\d{4})[/-](\d{2})[/-](\d{2})\s+(\d{2}):(\d{2})(?::(\d{2}))?", cleaned)
    if not m:
        return None
    yy, mm, dd, hh, mi, ss = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6) or "00"
    try:
        return datetime(int(yy), int(mm), int(dd), int(hh), int(mi), int(ss))
    except Exception:
        return None


def in_range(dt: Optional[datetime], start: datetime, end: datetime) -> bool:
    if dt is None:
        return False
    return start <= dt <= end


@dataclass
class Row:
    terminal: str
    carrier: str
    shipName: str
    voyage: str
    eta: str
    ata: str
    etd: str
    gateOpen: str
    gateCutoff: str


async def fetch_text(client: httpx.AsyncClient, url: str, *, encoding: Optional[str] = None) -> str:
    r = await client.get(url, timeout=30)
    r.raise_for_status()
    if encoding:
        return r.content.decode(encoding, errors="ignore")
    # let httpx handle apparent encoding
    return r.text


async def fetch_bpt(ship_name: str, start: datetime, end: datetime) -> List[Row]:
    """BPT: requires rendering inside iframe => Playwright."""
    target = "http://info.bptc.co.kr:9084/content/sw/frame/berth_status_text_frame_sw_kr.jsp"
    needle = normalize_ship_name(ship_name)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(target, wait_until="domcontentloaded", timeout=30000)

            s = {"y": str(start.year), "m": pad2(start.month), "d": pad2(start.day)}
            e = {"y": str(end.year), "m": pad2(end.month), "d": pad2(end.day)}

            await page.evaluate(
                """({s,e}) => {
                  const term = document.querySelector('input[type="radio"][name="v_time"][value="term"]');
                  if (term) term.click();
                  const setSelect = (name, val) => {
                    const el = document.querySelector(`select[name="${name}"]`);
                    if (el) {
                      el.value = val;
                      el.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                  };
                  setSelect('YEAR1', s.y);
                  setSelect('MONTH1', s.m);
                  setSelect('DAY1', s.d);
                  setSelect('YEAR2', e.y);
                  setSelect('MONTH2', e.m);
                  setSelect('DAY2', e.d);
                  const btn = document.querySelector('input[type="submit"][value="조회"]');
                  if (btn) btn.click();
                }""",
                {"s": s, "e": e},
            )

            await page.wait_for_function(
                """() => {
                  const iframe = document.querySelector('iframe[name="output"], iframe#output');
                  const doc = iframe?.contentDocument;
                  const table = doc?.querySelector('table');
                  return !!table && table.querySelectorAll('tr').length > 1;
                }""",
                timeout=30000,
            )

            payload = await page.evaluate(
                """() => {
                  const iframe = document.querySelector('iframe[name="output"], iframe#output');
                  const doc = iframe?.contentDocument;
                  const table = doc?.querySelector('table');
                  if (!table) return {headers:[], rows:[]};
                  const trs = Array.from(table.querySelectorAll('tr'));
                  const headerTr = trs.find(tr => tr.querySelectorAll('th').length > 0);
                  const headers = headerTr ? Array.from(headerTr.querySelectorAll('th')).map(th => th.textContent.trim()) : [];
                  const rows = trs
                    .filter(tr => tr.querySelectorAll('td').length > 0)
                    .map(tr => Array.from(tr.querySelectorAll('td')).map(td => td.textContent.replace(/\s+/g,' ').trim()));
                  return {headers, rows};
                }"""
            )

            headers = payload.get("headers", [])
            rows = payload.get("rows", [])

            def idx(name: str) -> int:
                try:
                    return headers.index(name)
                except ValueError:
                    return -1

            i_carrier = idx("선사")
            i_ship = idx("선박명")
            i_voy = idx("모선항차")
            i_eta = idx("입항예정일시")
            i_ata = idx("입항일시")
            i_etd = idx("출항일시")
            i_open = idx("반입시작일시")
            i_cut = idx("반입마감일시")

            out: List[Row] = []
            for r in rows:
                ship = r[i_ship] if i_ship >= 0 and i_ship < len(r) else ""
                if needle not in normalize_ship_name(ship):
                    continue
                out.append(
                    Row(
                        terminal="BPT",
                        carrier=r[i_carrier] if i_carrier >= 0 and i_carrier < len(r) else "",
                        shipName=ship,
                        voyage=r[i_voy] if i_voy >= 0 and i_voy < len(r) else "",
                        eta=r[i_eta] if i_eta >= 0 and i_eta < len(r) else "",
                        ata=r[i_ata] if i_ata >= 0 and i_ata < len(r) else "",
                        etd=r[i_etd] if i_etd >= 0 and i_etd < len(r) else "",
                        gateOpen=r[i_open] if i_open >= 0 and i_open < len(r) else "",
                        gateCutoff=r[i_cut] if i_cut >= 0 and i_cut < len(r) else "",
                    )
                )
            return out
        finally:
            await page.close()
            await browser.close()


async def fetch_gwct(client: httpx.AsyncClient, ship_name: str) -> List[Row]:
    url = "http://www.gwct.co.kr/e-service/ship/berth"
    needle = normalize_ship_name(ship_name)
    html = await fetch_text(client, url)
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table")
    if not table:
        return []

    headers = [th.get_text(strip=True) for th in table.find_all("th")]

    def idx(name: str) -> int:
        try:
            return headers.index(name)
        except ValueError:
            return -1

    i_carrier = idx("선사")
    i_ship = idx("선박명")
    i_voy = idx("모선항차")
    i_eta = idx("입항일시")
    i_etd = idx("출항일시")
    i_cut = idx("반입마감일시")

    out: List[Row] = []
    for tr in table.find_all("tr"):
        tds = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
        if not tds:
            continue
        ship = tds[i_ship] if i_ship >= 0 and i_ship < len(tds) else ""
        if needle not in normalize_ship_name(ship):
            continue
        out.append(
            Row(
                terminal="GWCT",
                carrier=tds[i_carrier] if i_carrier >= 0 and i_carrier < len(tds) else "",
                shipName=ship,
                voyage=tds[i_voy] if i_voy >= 0 and i_voy < len(tds) else "",
                eta=tds[i_eta] if i_eta >= 0 and i_eta < len(tds) else "",
                ata="",
                etd=tds[i_etd] if i_etd >= 0 and i_etd < len(tds) else "",
                gateOpen="",
                gateCutoff=tds[i_cut] if i_cut >= 0 and i_cut < len(tds) else "",
            )
        )
    return out


async def fetch_hktl(client: httpx.AsyncClient, ship_name: str) -> List[Row]:
    url = "https://custom.hktl.com/jsp/T01/sunsuk.jsp"
    needle = normalize_ship_name(ship_name)
    r = await client.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    # try utf-8 then euc-kr
    html = r.content.decode("utf-8", errors="ignore")
    if len(html) < 200:
        html = r.content.decode("euc-kr", errors="ignore")
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table")
    if not table:
        return []
    headers = [th.get_text(strip=True) for th in table.find_all("th")]

    def idx(name: str) -> int:
        try:
            return headers.index(name)
        except ValueError:
            return -1

    i_carrier = idx("선사")
    i_ship = idx("선박명")
    i_voy = idx("모선항차")
    i_eta = idx("입항예정일시")
    i_etd = idx("출항예정일시")
    i_cut = idx("반입마감일시")

    out: List[Row] = []
    for tr in table.find_all("tr"):
        tds = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
        if not tds:
            continue
        ship = tds[i_ship] if i_ship >= 0 and i_ship < len(tds) else ""
        if needle not in normalize_ship_name(ship):
            continue
        out.append(
            Row(
                terminal="HKTL",
                carrier=tds[i_carrier] if i_carrier >= 0 and i_carrier < len(tds) else "",
                shipName=ship,
                voyage=tds[i_voy] if i_voy >= 0 and i_voy < len(tds) else "",
                eta=tds[i_eta] if i_eta >= 0 and i_eta < len(tds) else "",
                ata="",
                etd=tds[i_etd] if i_etd >= 0 and i_etd < len(tds) else "",
                gateOpen="",
                gateCutoff=tds[i_cut] if i_cut >= 0 and i_cut < len(tds) else "",
            )
        )
    return out


async def fetch_snct(client: httpx.AsyncClient, ship_name: str) -> List[Row]:
    url = "https://snct.sun-kwang.co.kr/infoservice/webpage/vessel/vslScheduleText.jsp"
    needle = normalize_ship_name(ship_name)
    html = await fetch_text(client, url)
    soup = BeautifulSoup(html, "lxml")
    table = soup.select_one("#goosl_table")
    if not table:
        return []

    headers = [th.get_text(" ", strip=True) for th in table.select("thead th")]

    def idx(name: str) -> int:
        try:
            return headers.index(name)
        except ValueError:
            return -1

    i_carrier = idx("선사")
    i_ship = idx("선박명")
    i_voy = idx("모선항차")
    i_eta = idx("입항예정")
    i_etd = idx("출항예정")
    i_open = idx("반입시작")
    i_cut = idx("반입마감")

    def first_line(s: str) -> str:
        return (s or "").splitlines()[0].strip()

    out: List[Row] = []
    for tr in table.select("tbody tr"):
        tds = [td.get_text("\n", strip=True) for td in tr.select("td")]
        if not tds:
            continue
        ship = first_line(tds[i_ship]) if i_ship >= 0 and i_ship < len(tds) else ""
        if needle not in normalize_ship_name(ship):
            continue
        out.append(
            Row(
                terminal="SNCT(선광)",
                carrier=first_line(tds[i_carrier]) if i_carrier >= 0 and i_carrier < len(tds) else "",
                shipName=ship,
                voyage=(tds[i_voy].replace("\n", " ").strip() if i_voy >= 0 and i_voy < len(tds) else ""),
                eta=first_line(tds[i_eta]) if i_eta >= 0 and i_eta < len(tds) else "",
                ata="",
                etd=first_line(tds[i_etd]) if i_etd >= 0 and i_etd < len(tds) else "",
                gateOpen=first_line(tds[i_open]) if i_open >= 0 and i_open < len(tds) else "",
                gateCutoff=first_line(tds[i_cut]) if i_cut >= 0 and i_cut < len(tds) else "",
            )
        )
    return out


async def fetch_pctc(client: httpx.AsyncClient, ship_name: str, start: datetime, end: datetime) -> List[Row]:
    base = "http://www.pctc21.com/esvc/vessel/berthScheduleT/data"
    params = {
        "startDate": to_ymd_dash(start),
        "endDate": to_ymd_dash(end),
        "sort": "ETB",
        "page": "1",
    }
    needle = normalize_ship_name(ship_name)
    r = await client.get(base, params=params, timeout=30, headers={"Referer": "http://www.pctc21.com/esvc/vessel/berthScheduleT"})
    r.raise_for_status()
    j = r.json()
    content = j.get("content") or []
    out: List[Row] = []
    for it in content:
        ship = str(it.get("VSL_NM") or "")
        if needle not in normalize_ship_name(ship):
            continue
        voyage = it.get("OPR_VOY") if it.get("OPR_VOY") and it.get("OPR_VOY") != "-" else it.get("VOY_NO")
        out.append(
            Row(
                terminal="PCTC",
                carrier=str(it.get("IN_LANE") or it.get("PTNR_CODE") or ""),
                shipName=ship,
                voyage=str(voyage or ""),
                eta=str(it.get("ATA") or ""),
                ata="",
                etd=str(it.get("ATD") or ""),
                gateOpen="",
                gateCutoff=str(it.get("YARD_CLOSE") or ""),
            )
        )
    return out


async def fetch_dgt(client: httpx.AsyncClient, ship_name: str, start: datetime, end: datetime) -> List[Row]:
    page_url = "https://info.dgtbusan.com/DGT/esvc/vessel/berthScheduleT"
    api_url = "https://info.dgtbusan.com/DGT/esvc/vessel/vesselSchedule"
    needle = normalize_ship_name(ship_name)

    pres = await client.get(page_url, timeout=30)
    pres.raise_for_status()
    html = pres.text
    # cookie
    cookie = pres.headers.get("set-cookie", "")
    cookie = cookie.split(";", 1)[0] if cookie else ""

    m1 = re.search(r'meta name="_csrf" content="([^"]+)"', html, re.I)
    m2 = re.search(r'meta name="_csrf_header" content="([^"]+)"', html, re.I)
    token = m1.group(1) if m1 else ""
    header_name = m2.group(1) if m2 else "X-CSRF-TOKEN"
    if not token:
        return []

    body = {
        "fromDate": to_ymd_compact(start),
        "toDate": to_ymd_compact(end),
        "vessel": "",
        "voyage": "",
    }

    headers = {
        "Content-Type": "application/json",
        "Referer": page_url,
        header_name: token,
    }
    if cookie:
        headers["Cookie"] = cookie

    r = await client.post(api_url, json=body, headers=headers, timeout=30)
    r.raise_for_status()
    j = r.json()
    arr = j.get("vesselSchedules") or []

    out: List[Row] = []
    for it in arr:
        ship = str(it.get("vesselName") or "")
        if needle not in normalize_ship_name(ship):
            continue
        in_v = str(it.get("inVoyage") or "").strip()
        out_v = str(it.get("outVoyage") or "").strip()
        voyage = f"{in_v}/{out_v}" if in_v and out_v else (in_v or out_v)
        if not voyage:
            voyage_seq = str(it.get("voyageSeq") or "").strip()
            voyage_year = str(it.get("voyageYear") or "").strip()
            voyage = f"{voyage_seq}/{voyage_year}" if voyage_seq or voyage_year else ""

        out.append(
            Row(
                terminal="DGT",
                carrier=str(it.get("carrier") or it.get("serviceLane") or ""),
                shipName=ship,
                voyage=voyage,
                eta=str(it.get("etb") or it.get("eta") or ""),
                ata=str(it.get("ata") or ""),
                etd=str(it.get("atd") or it.get("etd") or ""),
                gateOpen="",
                gateCutoff=str(it.get("dischargeCloseDate") or it.get("loadCloseDate") or ""),
            )
        )
    return out


async def fetch_hjnc(client: httpx.AsyncClient, ship_name: str, start: datetime, end: datetime) -> List[Row]:
    base = "https://www.hjnc.co.kr/esvc/vessel/berthScheduleT/data"
    referer = "https://www.hjnc.co.kr/esvc/vessel/berthScheduleT"
    needle = normalize_ship_name(ship_name)

    params = {
        "startDate": to_ymd_dash(start),
        "endDate": to_ymd_dash(end),
        "sort": "ETB",
        "dateType": "",
        "route": "",
        "oper": "",
        "amount": "50",
        "page": "1",
    }
    headers = {
        "Referer": referer,
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json,text/plain,*/*",
    }

    r = await client.get(base, params=params, headers=headers, timeout=30)
    r.raise_for_status()
    j = r.json()
    raw = j.get("stringContent") or "[]"
    try:
        rows = json.loads(raw)
    except Exception:
        rows = []

    out: List[Row] = []
    for it in rows:
        ship = str(it.get("VSL_NM") or "")
        if needle not in normalize_ship_name(ship):
            continue
        voyage = it.get("OPR_VOY") if it.get("OPR_VOY") and it.get("OPR_VOY") != "-" else it.get("VOY_NO")
        out.append(
            Row(
                terminal="HJNC",
                carrier=str(it.get("PTNR_CODE") or ""),
                shipName=ship,
                voyage=str(voyage or ""),
                eta=str(it.get("ETB") or ""),
                ata=str(it.get("ATA") or ""),
                etd=str(it.get("ATD") or it.get("ETD") or ""),
                gateOpen=str(it.get("YARD_OPEN") or ""),
                gateCutoff=str(it.get("YARD_CLOSE") or ""),
            )
        )
    return out


async def fetch_hpnt(client: httpx.AsyncClient, ship_name: str) -> List[Row]:
    url = "https://www.hpnt.co.kr/infoservice/vessel/vslScheduleList.jsp"
    needle = normalize_ship_name(ship_name)

    html = await fetch_text(client, url)
    soup = BeautifulSoup(html, "lxml")

    # find schedule table by header row containing 선석/선사/선명
    table = None
    for t in soup.find_all("table"):
        ths = [th.get_text(strip=True) for th in t.find_all("th")]
        if "선석" in ths and "선사" in ths and "선명" in ths:
            table = t
            break
    if not table:
        return []

    out: List[Row] = []
    trs = table.find_all("tr")
    for tr in trs[1:]:
        tds = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
        if len(tds) < 9:
            continue
        ship = tds[4]
        if needle not in normalize_ship_name(ship):
            continue
        voyage = " ".join([x for x in [tds[2], tds[3]] if x])
        out.append(
            Row(
                terminal="HPNT",
                carrier=tds[1],
                shipName=ship,
                voyage=voyage,
                gateCutoff=tds[6],
                eta=tds[7],
                ata="",
                etd=tds[8],
                gateOpen="",
            )
        )
    return out


async def fetch_juct(client: httpx.AsyncClient, ship_name: str) -> List[Row]:
    list_url = "https://www.juct.co.kr/web/NEW/schedule/index.asp"
    needle = normalize_ship_name(ship_name)

    r = await client.get(list_url, timeout=30)
    r.raise_for_status()
    # try euc-kr then utf-8
    html = r.content.decode("euc-kr", errors="ignore")
    if len(html) < 200:
        html = r.content.decode("utf-8", errors="ignore")

    soup = BeautifulSoup(html, "lxml")
    chosen = None
    for t in soup.find_all("table"):
        # JUCT uses td headers in first row
        first = t.find("tr")
        if not first:
            continue
        hdrs = [td.get_text(strip=True) for td in first.find_all("td")]
        if "모선코드/항차" in hdrs and "입항예정일시" in hdrs and "출항예정일시" in hdrs and "모선명" in hdrs:
            chosen = t
            break
    if not chosen:
        return []

    candidates: List[Dict[str, Any]] = []
    for tr in chosen.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) != 7:
            continue
        code_text = tds[0].get_text(strip=True)
        ship = tds[5].get_text(strip=True)
        if needle not in normalize_ship_name(ship):
            continue
        href = ""
        a = tds[0].find("a")
        if a and a.has_attr("href"):
            href = a["href"]
        m = re.search(r"showDetail\('([^']+)'\)", href)
        arg = m.group(1) if m else None
        candidates.append(
            {
                "codeText": code_text,
                "arg": arg,
                "eta": tds[1].get_text(strip=True),
                "etd": tds[2].get_text(strip=True),
                "shipName": ship,
            }
        )

    out: List[Row] = []
    for c in candidates:
        carrier = ""
        ata = ""
        gate_cut = ""
        eta = c["eta"]
        etd = c["etd"]

        if c.get("arg"):
            detail_url = f"https://www.juct.co.kr/web/NEW/schedule/detail.asp?arg={httpx.QueryParams({'arg':c['arg']})['arg']}"
            dres = await client.get(detail_url, timeout=30)
            dres.raise_for_status()
            dhtml = dres.content.decode("euc-kr", errors="ignore")
            if len(dhtml) < 200:
                dhtml = dres.content.decode("utf-8", errors="ignore")
            dsoup = BeautifulSoup(dhtml, "lxml")

            def get_pair(label: str) -> str:
                td = dsoup.find("td", string=lambda s: (s or "").strip() == label)
                if not td:
                    return ""
                nxt = td.find_next_sibling("td")
                return nxt.get_text(" ", strip=True) if nxt else ""

            carrier = get_pair("업체코드")
            eta = get_pair("입항예정일시") or eta
            etd = get_pair("출항예정일시") or etd
            ata = get_pair("입항일시") or ""
            atd = get_pair("출항일시") or ""
            gate_cut = get_pair("Closing Time") or ""
            if atd:
                etd = atd

        out.append(
            Row(
                terminal="JUCT",
                carrier=carrier,
                shipName=c["shipName"],
                voyage=c["codeText"],
                eta=eta,
                ata=ata,
                etd=etd,
                gateOpen="",
                gateCutoff=gate_cut,
            )
        )

    return out


async def search_ship_schedules(ship_name: str, *, start: Optional[datetime] = None, end: Optional[datetime] = None) -> Dict[str, Any]:
    name = (ship_name or "").strip()
    if not name:
        raise ValueError("shipName is required")

    now = datetime.now()
    sd = start or datetime(now.year, now.month, now.day) - timedelta(days=2)
    sd = sd.replace(hour=0, minute=0, second=0, microsecond=0)
    ed = end or (datetime(now.year, now.month, now.day) + timedelta(days=7))
    ed = ed.replace(hour=23, minute=59, second=59, microsecond=0)

    async with httpx.AsyncClient(follow_redirects=True, headers={"User-Agent": "Mozilla/5.0"}) as client:
        tasks = [
            fetch_bpt(name, sd, ed),
            fetch_gwct(client, name),
            fetch_hktl(client, name),
            fetch_snct(client, name),
            fetch_pctc(client, name, sd, ed),
            fetch_dgt(client, name, sd, ed),
            fetch_hjnc(client, name, sd, ed),
            fetch_hpnt(client, name),
            fetch_juct(client, name),
        ]

        # 실패는 숨김(기존 API 룰)
        gathered = await asyncio.gather(*tasks, return_exceptions=True)

    rows: List[Row] = []
    for r in gathered:
        if isinstance(r, Exception):
            continue
        rows.extend(r)

    # 공통 날짜 필터
    filtered: List[Dict[str, str]] = []
    for row in rows:
        eta = parse_korean_like_datetime(row.eta)
        ata = parse_korean_like_datetime(row.ata)
        etd = parse_korean_like_datetime(row.etd)
        if in_range(eta, sd, ed) or in_range(ata, sd, ed) or in_range(etd, sd, ed):
            filtered.append(row.__dict__)

    return {
        "ok": True,
        "query": {"shipName": name},
        "range": {"start": to_ymd_dash(sd), "end": to_ymd_dash(ed)},
        "results": filtered,
    }
