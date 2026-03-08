from __future__ import annotations

from chn_stat.pipeline import build_proxy_salary_series


def main() -> None:
    frame = build_proxy_salary_series()
    print(frame.to_string(index=False))


if __name__ == "__main__":
    main()
