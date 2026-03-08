from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from chn_stat.plotting import _configure_font


EDUCATION_LABELS_EN = {
    "college": "Associate",
    "bachelor": "Bachelor",
    "master": "Master",
    "doctor": "Doctoral",
}

EDUCATION_LABELS_ZH = {
    "college": "大专",
    "bachelor": "本科",
    "master": "硕士研究生",
    "doctor": "博士研究生",
}

EDUCATION_COLORS = {
    "college": "#4C6A92",
    "bachelor": "#2A9D8F",
    "master": "#E9C46A",
    "doctor": "#D55D4C",
}


def generate_survey_year_outputs(
    frame,
    output_dir: Path,
    *,
    stem: str,
) -> tuple[Path, Path]:
    if frame.empty:
        raise ValueError("Survey-year output frame is empty.")

    output_dir.mkdir(parents=True, exist_ok=True)
    has_cjk_font = _configure_font()
    labels = EDUCATION_LABELS_ZH if has_cjk_font else EDUCATION_LABELS_EN
    title = (
        "调查年份学历工资汇总图"
        if has_cjk_font
        else "Survey-Year Wage Summary by Education"
    )
    ylabel = "年工资（元）" if has_cjk_font else "Annual wage (RMB)"

    csv_path = output_dir / f"{stem}.csv"
    png_path = output_dir / f"{stem}.png"
    frame.to_csv(csv_path, index=False, encoding="utf-8-sig")

    figure, axis = plt.subplots(figsize=(11, 6.5), layout="constrained")
    line_styles = ["-", "--", "-.", ":"]
    sources = list(dict.fromkeys(frame["source"]))
    source_styles = {source: line_styles[index % len(line_styles)] for index, source in enumerate(sources)}

    for source in sources:
        source_frame = frame[frame["source"] == source]
        for education_level in ["college", "bachelor", "master", "doctor"]:
            education_frame = source_frame[source_frame["education_level"] == education_level]
            if education_frame.empty:
                continue
            axis.plot(
                education_frame["survey_year"],
                education_frame["mean_annual_wage"],
                marker="o",
                linewidth=2.2,
                linestyle=source_styles[source],
                color=EDUCATION_COLORS[education_level],
                label=f"{source.upper()} {labels[education_level]}",
            )

    figure.suptitle(title, x=0.09, y=0.99, ha="left", fontsize=16, fontweight="bold")
    axis.set_xlabel("Survey year")
    axis.set_ylabel(ylabel)
    axis.grid(axis="y", linestyle="--", alpha=0.35)
    axis.legend(frameon=False, ncols=2, loc="upper left", bbox_to_anchor=(0.0, 0.995))
    figure.savefig(png_path, dpi=180, bbox_inches="tight")
    plt.close(figure)
    return csv_path, png_path
