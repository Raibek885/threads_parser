from scraper import get_threads_html
from parser import parse_threads_page
from exporter import export_to_csv, export_to_json

def main():
    keywords = ["Qasqelen", "SDU", "Dimash"]  # put any keywords you want to search for
    all_posts = []

    for kw in keywords:
        print(f"\n[🔍] Start parsing via keyworld: {kw}")
        html = get_threads_html(kw)
        posts = parse_threads_page(html, kw)
        all_posts.extend(posts)
        print(f"[+] recognized {len(posts)} posts by '{kw}'")

    export_to_csv(all_posts)
    export_to_json(all_posts)
    print("\n✅ Ready!")

if __name__ == "__main__":
    main()