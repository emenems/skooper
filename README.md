# SKooper

**Scooping Slovak news stories & comment**

Welcome to **SKooper**, the HTML scraper for fetching Slovak news articles, their juicy comments, and analyzing the lot—all in the beautiful Slovak language. Whether you're a researcher, a media junkie, or just curious about what’s buzzing in Slovakia, SKooper’s got your back.

---

## News outlets
- **Pravda.sk** Extracts full news article content from [pravda.sk](pravda.sk) website.

---

## Install & Run

1. Clone the Repo:
   ```bash
   git clone https://github.com/emenems/skooper
   cd skooper
   ```

2. Install dependencies:
   ```bash
   python -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

3. Run locally:
   ```bash
   uvicorn src.api.main:app --reload
   ```
