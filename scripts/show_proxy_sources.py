from __future__ import annotations

from chn_stat.pipeline import load_education_proxy, load_official_wages


def main() -> None:
    official = load_official_wages()
    education = load_education_proxy()

    print("Official wage sources:")
    for year in sorted(official):
        entry = official[year]
        non_private = entry["non_private"]
        private = entry["private"]
        print(f"- {year} non-private: {non_private['value']} | {non_private['url']}")
        print(f"- {year} private: {private['value']} | {private['url']}")

    print("\nEducation proxy source:")
    print(f"- {education['report_title']} | {education['source_url']}")


if __name__ == "__main__":
    main()
