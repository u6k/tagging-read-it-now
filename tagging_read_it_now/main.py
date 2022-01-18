import json
import logging
import logging.config
import os
import warnings

import requests

# グローバル設定
LINKACE_HEADERS = {
    "Authorization": f"Bearer {os.environ['LINKACE_API_TOKEN']}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}
LINKACE_TAG_READ_IT_LATER = int(os.environ["LINKACE_TAG_READ_IT_LATER"])
LINKACE_TAG_READ_IT_NOW = int(os.environ["LINKACE_TAG_READ_IT_NOW"])


# ログ設定
logging.config.dictConfig({
    "version": 1,

    "formatters": {
        "tagging_read_it_now.logging.format": {
            "format": "%(asctime)s - %(levelname)-5s [%(name)s] %(message)s",
        },
    },

    "handlers": {
        "tagging_read_it_now.logging.handler": {
            "class": "logging.StreamHandler",
            "formatter": "tagging_read_it_now.logging.format",
            "level": logging.DEBUG,
        },
    },

    "loggers": {
        "tagging_read_it_now": {
            "handlers": ["tagging_read_it_now.logging.handler"],
            "level": logging.DEBUG,
            "propagate": 0,
        },
    },
})

L = logging.getLogger("tagging_read_it_now")

warnings.simplefilter("ignore")


def get_read_it_later_bookmarks(req_url=None):
    L.info(f"get_read_it_later_bookmarks: start: page={req_url}")

    if not req_url:
        req_url = f"https://bookmark.u6k.me/api/v1/search/links?only_tags={LINKACE_TAG_READ_IT_LATER}&order_by=created_at:desc"

    res = requests.get(
        req_url,
        headers=LINKACE_HEADERS,
    )

    if res.status_code != 200:
        raise RuntimeError(res.status_code)

    res_json = res.json()

    result = {
        "next_page_url": res_json["next_page_url"],
        "data": [],
    }

    for d in res_json["data"]:
        result["data"].append({
            "id": d["id"],
            "url": d["url"],
            "title": d["title"],
        })

    return result


def tagging_read_it_now(bookmark_id):
    L.info(f"tagging_read_it_now: start: bookmark_id={bookmark_id}")

    # ブックマーク詳細を取得する
    res = requests.get(
        f"https://bookmark.u6k.me/api/v1/links/{bookmark_id}",
        headers=LINKACE_HEADERS,
    )

    if res.status_code != 200:
        L.error(res.status_code)
        L.error(res.text)
        raise RuntimeError

    # タグにread it nowが含まれるか確認する
    res_json = res.json()
    L.debug({
        "id": res_json["id"],
        "title": res_json["title"],
    })

    lists = [li["id"] for li in res_json["lists"]]
    tags = [t["id"] for t in res_json["tags"]]

    if LINKACE_TAG_READ_IT_NOW in tags:
        L.debug("include read_it_now")
        return False

    # タグにread it nowを付けて更新する
    tags.append(LINKACE_TAG_READ_IT_NOW)

    req_params = {
        "url": res_json["url"],
        "lists": lists,
        "tags": tags,
        "is_private": res_json["is_private"],
    }

    res = requests.patch(
        f"https://bookmark.u6k.me/api/v1/links/{bookmark_id}",
        headers=LINKACE_HEADERS,
        data=json.dumps(req_params),
    )

    if res.status_code != 200:
        L.error(res.status_code)
        L.error(res.text)
        raise RuntimeError

    L.debug("bookmark updated")

    return True


# メイン処理
if __name__ == "__main__":
    updated_count = 0
    bookmarks = None
    count_of_items = int(os.environ["COUNT_OF_ITEMS"])

    while updated_count < count_of_items:
        if bookmarks:
            bookmarks = get_read_it_later_bookmarks(bookmarks["next_page_url"])
        else:
            bookmarks = get_read_it_later_bookmarks()

        for bookmark in bookmarks["data"]:
            result = tagging_read_it_now(bookmark["id"])

            if result:
                updated_count += 1

            if updated_count >= count_of_items:
                break
