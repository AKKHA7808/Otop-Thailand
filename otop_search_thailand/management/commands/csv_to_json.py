import csv
import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Convert CSV/Excel (optional) to JSON array of objects for OTOP data."

    def add_arguments(self, parser):
        parser.add_argument("input_path", type=str, help="Path to CSV/XLSX")
        parser.add_argument(
            "-o",
            "--output",
            type=str,
            default=None,
            help="Output JSON path (default: same name .json)",
        )
        parser.add_argument("--encoding", type=str, default="utf-8-sig", help="CSV encoding")
        parser.add_argument(
            "--sheet", type=str, default=None, help="Excel sheet name/index (optional)"
        )

    def handle(self, *args, **opts):
        in_path = Path(opts["input_path"])
        out_path = opts["output"]
        if not in_path.exists():
            raise CommandError(f"Input not found: {in_path}")
        if not out_path:
            out_path = str(in_path.with_suffix(".json"))
        ext = in_path.suffix.lower()

        if ext == ".csv":
            with in_path.open("r", encoding=opts["encoding"], newline="") as f:
                rows = list(csv.DictReader(f))
        elif ext in (".xlsx", ".xls"):
            try:
                import pandas as pd
            except Exception:
                raise CommandError(
                    "Reading Excel requires pandas + openpyxl: pip install pandas openpyxl"
                )
            df = pd.read_excel(in_path, sheet_name=opts["sheet"] if opts["sheet"] else 0)
            rows = df.to_dict(orient="records")
        else:
            raise CommandError("Unsupported input type. Use .csv or .xlsx/.xls")

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)
        self.stdout.write(self.style.SUCCESS(f"Wrote JSON → {out_path}"))
