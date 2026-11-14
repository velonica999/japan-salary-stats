"""給料相場.com の /data/ から集計済み CSV を取り込む（毎日 GitHub Actions が実行）。

安全のための決まり：
- 取りに行く先は https://kyuryo-souba.com/data/ の決まったファイルだけ（URL は下に固定）。
- 1つでも検査に通らなければ、何も書き換えずに終了する（前の CSV がそのまま残る）。
- 検査：HTTP 200・UTF-8（BOM 付き）・1行目が期待どおりの列名・行数が前回の 90% 以上・容量 25MB 以下。
- 鍵やトークンは使わない（公開ページを読むだけ）。
- 容量の見張り：どれかの CSV が 20MB を超えたら、このリポジトリに Issue を1件立てる（運営者に GitHub からメールが届く）。
  Cloudflare Pages の上限は1ファイル 25MiB。サイト側（generate.py）は 23MB を超えると推移の CSV を古い年から自動で削る。
  Issue が来たらファイルの分け方を見直す（推移の CSV を年ごとに分けるなど）。
"""
import csv
import io
import json
import os
import sys
import urllib.request

BASE = "https://kyuryo-souba.com/data/"
FILES = {
    "occupation_prefecture_latest.csv": "調査年,職種コード,職種名,職種名_略称,大分類コード,大分類名,都道府県コード,都道府県名,性別,",
    "occupation_prefecture_yearly.csv": "調査年,職種コード,職種名_略称,大分類コード,都道府県コード,都道府県名,性別,",
    "major_prefecture_yearly.csv": "調査年,大分類コード,大分類名,都道府県コード,都道府県名,性別,",
    "prefecture_yearly.csv": "調査年,都道府県コード,都道府県名,性別,",
    "occupation_age_latest.csv": "調査年,職種コード,職種名,職種名_略称,年齢階級,",
}
MAX_BYTES = 25 * 1024 * 1024
WARN_BYTES = 20_000_000
ISSUE_TITLE = "CSV の容量が 20MB を超えました（構成の見直しが必要）"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def rows(b):
    return sum(1 for _ in csv.reader(io.StringIO(b.decode("utf-8-sig")))) - 1


def size_alert(big):
    """20MB を超えた CSV があれば Issue を立てる（同じ題の Issue が開いていれば何もしない）。失敗しても取り込みは止めない"""
    token, repo = os.environ.get("GITHUB_TOKEN"), os.environ.get("GITHUB_REPOSITORY")
    if not big or not token or not repo:
        return
    api = f"https://api.github.com/repos/{repo}/issues"
    hd = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json", "User-Agent": "japan-salary-stats-sync"}
    try:
        with urllib.request.urlopen(urllib.request.Request(api + "?state=open&per_page=100", headers=hd), timeout=30) as r:
            if any(i.get("title") == ISSUE_TITLE for i in json.load(r)):
                print("容量の Issue は既に開いている")
                return
        body = ("次の CSV が 20MB を超えました。Cloudflare Pages の上限は1ファイル 25MiB です。\n\n"
                + "\n".join(f"- {fn}: {sz / 1e6:.1f}MB" for fn, sz in big)
                + "\n\nサイト側は 23MB を超えると推移の CSV を古い年から自動で削るので、サイトが止まることはありません。"
                "ただし古い年が消えていくので、ファイルの分け方を見直してください"
                "（推移の CSV を年ごとのファイルに分けるなど）。直したらこの Issue を閉じてください。")
        req = urllib.request.Request(api, data=json.dumps({"title": ISSUE_TITLE, "body": body}).encode(), headers=hd, method="POST")
        with urllib.request.urlopen(req, timeout=30):
            print("::warning::容量の Issue を立てた")
    except Exception as e:
        print(f"::warning::容量の Issue を立てられなかった：{e}")


def main():
    got, ng = {}, []
    for fn, head in FILES.items():
        try:
            req = urllib.request.Request(BASE + fn, headers={"User-Agent": "japan-salary-stats-sync (+https://github.com/velonica999/japan-salary-stats)"})
            with urllib.request.urlopen(req, timeout=60) as r:
                if r.status != 200:
                    ng.append(f"{fn}: HTTP {r.status}")
                    continue
                b = r.read(MAX_BYTES + 1)
        except Exception as e:
            ng.append(f"{fn}: 取得失敗 {e}")
            continue
        if len(b) > MAX_BYTES:
            ng.append(f"{fn}: 25MB を超えた")
            continue
        if not b.startswith(b"\xef\xbb\xbf"):
            ng.append(f"{fn}: BOM 付き UTF-8 ではない（HTML のエラーページなどの恐れ）")
            continue
        try:
            text = b.decode("utf-8-sig")
        except UnicodeDecodeError:
            ng.append(f"{fn}: UTF-8 として読めない")
            continue
        if not text.startswith(head):
            ng.append(f"{fn}: 列名が想定と違う：{text.splitlines()[0][:120]}")
            continue
        n = rows(b)
        old = os.path.join(OUT, fn)
        if os.path.exists(old):
            n_old = rows(open(old, "rb").read())
            if n < n_old * 0.9:
                ng.append(f"{fn}: 行数が急に減った（{n_old:,} → {n:,}）")
                continue
        got[fn] = (b, n)
    if ng:
        for m in ng:
            print(f"::error::{m}")
        print("取り込みを中止（前の CSV のまま）")
        sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    for fn, (b, n) in got.items():
        with open(os.path.join(OUT, fn), "wb") as f:
            f.write(b)
        print(f"{fn}: {n:,} 行・{len(b) / 1e6:.1f}MB")
    size_alert([(fn, len(b)) for fn, (b, n) in got.items() if len(b) > WARN_BYTES])


if __name__ == "__main__":
    main()
