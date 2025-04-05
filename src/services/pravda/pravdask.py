from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import re
from datetime import datetime, timedelta
from src.utils.fetch import fetch_html


class PravdaSK:
    def __init__(self, article_url: str):
        """Initialize with a 'dirty' URL and clean it."""
        self.source = "pravdask"
        self.cleaned_url = self._url_cleanup(article_url)
        self.debate_url = self.get_debate_url(self.cleaned_url)

    def _url_cleanup(self, url: str) -> str:
        """
        Clean up the given URL for processing.

        Args:
            url: The URL to clean up

        Returns:
            Cleaned URL

        Raises:
            ValueError: If URL is invalid
        """
        if not url.startswith("https://") or "pravda" not in url:
            raise ValueError("Invalid URL. Must start with 'https://' and contain 'pravda'.")
        url = re.sub(r"\?.*$", "", url)
        if not url.endswith("/"):
            url += "/"
        return url

    def get_debate_url(self, article_url: str) -> str:
        """Generate debate URL from article URL."""
        pattern = r"clanok/(\d+)-(.+)/$"
        match = re.search(pattern, article_url)
        if not match:
            raise ValueError("Invalid pravda.sk article URL")
        article_id, title = match.groups()
        return f"https://debata.pravda.sk/debata/{article_id}-{title}/"

    def _extract_datetime(self, date_html: str) -> str:
        """Extract and format datetime from HTML content."""
        datetime_str = ""
        if date_html:
            time_match = re.search(r"<br/>(\d{1,2}:\d{2})</span>", str(date_html))
            time_text = time_match.group(1) if time_match else ""
            if "dnes" in str(date_html):
                date_text = datetime.now().strftime("%d.%m.%Y")
            elif "včera" in str(date_html):
                date_text = (datetime.now() - timedelta(days=1)).strftime("%d.%m.%Y")
            else:
                date_match = re.search(r"\s*(\d{1,2}\.\d{1,2}\.\d{4})\s*", str(date_html))
                date_text = date_match.group(1) if date_match else ""
            datetime_str = f"{date_text} {time_text}"
        return datetime_str

    def _extract_rating(self, rating_html) -> str:
        """Extract rating from HTML content."""
        return rating_html.get_text(strip=True) if rating_html else "0"

    def _extract_author(self, author_html) -> str:
        """Extract author from HTML content."""
        return author_html.get_text(strip=True) if author_html else "Anonymous"

    def parse_post(self, post: BeautifulSoup, parent_id: Optional[str], existing_posts: List[dict]) -> List[dict]:
        """
        Recursively parse a post and its replies.

        Args:
            post: BeautifulSoup object representing the post
            parent_id: ID of the parent post (None for top-level posts)
            existing_posts: List to store parsed post data

        Returns:
            List of parsed posts
        """
        post_id = post.get("id", "").replace("prispevok_", "")
        if post_id in set(i["post_id"] for i in existing_posts):
            return existing_posts

        content_div = post.find("div", class_="post")
        if not content_div:
            return existing_posts

        post_data = {
            "post_id": post_id,
            "author": self._extract_author(post.find("a", class_="comment-author")),
            "text": "\n".join([p.get_text(strip=True) for p in content_div.find_all("p")]),
            "rating": self._extract_rating(post.find("div", class_="rating")),
            "timestamp": self._extract_datetime(post.find("span", class_="comment-time")),
            "parent_id": parent_id,
            "article_url": self.cleaned_url,
            "source": self.source,
        }

        existing_posts.append(post_data)

        post_list = post.find("div", class_="postList")
        if post_list:
            replies = post_list.find_all("div", class_="post", recursive=False)
            for reply in replies:
                self.parse_post(reply, post_id, existing_posts)

        return existing_posts

    def parse_article(self) -> dict:
        """
        Parse article content using the cleaned URL.

        Returns:
            Dictionary containing title, description, and body
        """
        response_text = fetch_html(self.cleaned_url)
        soup = BeautifulSoup(response_text, "html.parser")

        title = soup.find("h1").get_text(strip=True) if soup.find("h1") else ""
        description_tag = soup.find("p", itemprop="description")
        description = description_tag.get_text(strip=True) if description_tag else ""
        body_div = soup.find("div", itemprop="articleBody")
        body = "\n".join([p.get_text(strip=True) for p in body_div.find_all("p")]) if body_div else ""

        return {
            "title": title,
            "description": description,
            "body": body,
            "article_url": self.cleaned_url,
            "source": self.source,
        }

    def scrape_comments(self) -> List[Dict]:
        """
        Scrape comments using the debate URL.

        Returns:
            List of comment dictionaries
        """
        comments = []
        page = 1
        max_post_per_page = 20
        post_nr = 20

        while page <= 500 and post_nr == max_post_per_page:
            url = (
                self.debate_url
                if page == 1
                else f"{self.debate_url}?view_mode=vlakna&ordering=od_najnovsieho&strana={page}"
            )
            response_text = fetch_html(url)
            soup = BeautifulSoup(response_text, "html.parser")
            post_list = soup.find("div", class_="postList")

            if not post_list or not post_list.find_all("div", class_="post"):
                break

            page_comments = []
            for post_nr, post in enumerate(post_list.find_all("div", class_="post", recursive=False), 1):
                page_comments = self.parse_post(post, None, page_comments)

            if not page_comments:
                break

            comments.extend(page_comments)
            page += 1

        return comments
