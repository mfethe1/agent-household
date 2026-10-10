"""Synthetic cases prove grammar correctness, not live retailer compatibility."""

import unittest
from typing import cast

from agent_household.target_url import validate_product_url


class TargetURLTests(unittest.TestCase):
    def rejects(self, url: object, tcin: object) -> None:
        with self.assertRaises(ValueError) as caught:
            validate_product_url(cast(str, url), cast(str, tcin))
        self.assertEqual(str(caught.exception), "invalid Target product URL")

    def test_canonical_identity(self) -> None:
        for slug, tcin in (
            ("synthetic-rice", "54602335"),
            ("a", "54602335"),
            ("a2-b3", "54602335"),
            ("a" * 160, "54602335"),
            ("a-" * 79 + "aa", "54602335"),
            ("synthetic", "00000001"),
        ):
            url = f"https://www.target.com/p/{slug}/-/A-{tcin}"
            with self.subTest(slug=slug, tcin=tcin):
                self.assertIs(validate_product_url(url, tcin), url)

    def test_unsafe_urls(self) -> None:
        url = "https://www.target.com/p/synthetic-rice/-/A-54602335"
        bad = [
            url.replace("/-/", "/"),
            url.replace("54602335", "54602336"),
            url + "?preselect=54602335",
            url + "?",
            url + "#fragment",
            url + "#",
            url + "/",
            url + "\n",
            url + " ",
            " " + url,
            url.replace("www.target.com", "user:sentinel@www.target.com"),
            url.replace("www.target.com", "www.target.com.evil"),
            url.replace("www.target.com", "www-target.com"),
            url.replace("www.target.com", "wwwxtarget.com"),
            url.replace("www.target.com", "www.targetxcom"),
            url.replace("www.target.com", "target.com"),
            url.replace("https:", "http:"),
            url.replace("https:", "file:"),
            url.replace("https:", "data:"),
            url.replace("www.target.com", "www.target.com:443"),
            url.replace("www.target.com", "www.target.com:8080"),
            url.replace("www.target.com", "127.0.0.1"),
            url.replace("www.target.com", "WWW.TARGET.COM"),
            url.replace("https", "HTTPS"),
            url.replace("/p/", "/P/"),
            url.replace("/-/A-", "/-/a-"),
            url.replace("synthetic", "Synthetic"),
            url.replace("target", "t\u0430rget"),
            url.replace("synthetic", "synthetic\u200b"),
            url.replace("54602335", "\uff15\uff14\uff16\uff10\uff12\uff13\uff13\uff15"),
            url.replace("/-/", "/%2F/"),
            url.replace("www.target.com", "www%2etarget.com"),
            url.replace("/p/", "/%70/"),
            url.replace("/p/", "/account/"),
            url.replace("/p/", "//p/"),
            url.replace("/p/", "/p/../"),
            url.replace("synthetic-rice", ""),
            url.replace("synthetic-rice", "synthetic_rice"),
            url.replace("synthetic-rice", "-synthetic"),
            url.replace("synthetic-rice", "synthetic-"),
            url.replace("synthetic-rice", "synthetic--rice"),
            url.replace("synthetic-rice", "a" * 161),
            url.replace("synthetic-rice", "a-" * 80 + "a"),
            url.replace("synthetic-rice", "a" * 513),
            url.replace("54602335", "5460233"),
            url.replace("54602335", "546023355"),
            url.replace("synthetic", "synthetic\x00"),
            url.replace("synthetic", "synthetic\t"),
        ]
        for item in bad:
            with self.subTest(url=item):
                self.rejects(item, "54602335")

    def test_invalid_types_and_tcin(self) -> None:
        class DerivedStr(str):
            pass

        url = "https://www.target.com/p/synthetic-rice/-/A-54602335"
        for item in (
            "5460233",
            "546023355",
            "\uff15\uff14\uff16\uff10\uff12\uff13\uff13\uff15",
            "54602335\n",
        ):
            with self.subTest(tcin=item):
                self.rejects(url, item)
        for item in (1, True, b"54602335", None, DerivedStr("54602335")):
            with self.subTest(tcin=item):
                self.rejects(url, item)
        for item in (1, True, url.encode(), None, DerivedStr(url)):
            with self.subTest(url=item):
                self.rejects(item, "54602335")
        for item in (
            "\uff15\uff14\uff16\uff10\uff12\uff13\uff13\uff15",
            "\u0665\u0664\u0666\u0660\u0662\u0663\u0663\u0665",
        ):
            with self.subTest(matching_non_ascii=item):
                self.rejects(url.replace("54602335", item), item)


if __name__ == "__main__":
    unittest.main()
