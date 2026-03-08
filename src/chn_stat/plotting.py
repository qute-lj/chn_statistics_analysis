from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager

from chn_stat.pipeline import build_proxy_salary_series


def _configure_font() -> bool:
    candidates = [
        "Noto Sans CJK SC",
        "Source Han Sans SC",
        "Microsoft YaHei",
        "SimHei",
        "WenQuanYi Zen Hei",
        "PingFang SC",
        "STHeiti",
    ]
    available = {font.name for font in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.family"] = name
            plt.rcParams["axes.unicode_minus"] = False
            return True
    plt.rcParams["axes.unicode_minus"] = False
    return False


def generate_outputs(output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    has_cjk_font = _configure_font()
    frame = build_proxy_salary_series()

    csv_path = output_dir / "education_wage_proxy_2016_2024.csv"
    png_path = output_dir / "education_wage_proxy_2016_2024.png"
    frame.to_csv(csv_path, index=False, encoding="utf-8-sig")

    labels = (
        {
            "title": "2016-2024 China Wage Trend by Education (Proxy)",
            "college": "Associate",
            "bachelor": "Bachelor",
            "master": "Master",
            "doctor": "Doctoral",
            "ylabel": "Annual wage (RMB)",
            "footer": (
                "Approximation only. Based on official NBS wage bulletins and 2024 public\n"
                "education proxy spacing. 2025 omitted because the official 2025 wage "
                "bulletin had not been released as of 2026-03-08."
            ),
        }
        if not has_cjk_font
        else {
            "title": "2016-2024年中国不同学历工资变化图（近似）",
            "college": "大专",
            "bachelor": "本科",
            "master": "硕士研究生",
            "doctor": "博士研究生",
            "ylabel": "年工资（元）",
            "footer": (
                "说明：本图基于国家统计局工资公告与2024公开学历薪酬代理系数，为近似推算，\n"
                "不是国家统计局直接发布的学历工资序列；"
                "2025年官方年平均工资公报截至2026-03-08尚未发布。"
            ),
        }
    )

    figure, axis = plt.subplots(figsize=(11, 6.5), layout="constrained")
    colors = {
        "college": "#4C6A92",
        "bachelor": "#2A9D8F",
        "master": "#E9C46A",
        "doctor": "#D55D4C",
    }
    for column in ["college", "bachelor", "master", "doctor"]:
        axis.plot(
            frame["year"],
            frame[column],
            marker="o",
            linewidth=2.2,
            color=colors[column],
            label=labels[column],
        )

    figure.suptitle(labels["title"], x=0.09, y=0.99, ha="left", fontsize=16, fontweight="bold")
    axis.set_xlabel("Year")
    axis.set_ylabel(labels["ylabel"])
    axis.grid(axis="y", linestyle="--", alpha=0.35)
    axis.set_xticks(frame["year"])
    axis.legend(frameon=False, ncols=2, loc="upper left", bbox_to_anchor=(0.0, 0.995))
    axis.text(
        0.0,
        -0.18,
        labels["footer"],
        transform=axis.transAxes,
        fontsize=9,
        color="#4f4f4f",
        va="top",
    )
    figure.savefig(png_path, dpi=180, bbox_inches="tight")
    plt.close(figure)

    return csv_path, png_path
