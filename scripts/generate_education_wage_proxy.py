from __future__ import annotations

from pathlib import Path

from chn_stat.plotting import generate_outputs


def main() -> None:
    output_dir = Path.cwd() / "outputs"
    csv_path, png_path = generate_outputs(output_dir)
    print(f"CSV written to: {csv_path}")
    print(f"PNG written to: {png_path}")


if __name__ == "__main__":
    main()
