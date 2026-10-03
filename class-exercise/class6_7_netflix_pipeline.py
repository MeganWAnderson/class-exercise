import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from class6_7_netflix_utils import (
    drop_missing_rows,
    remove_duplicates,
    remove_iqr_outliers, 
    show_overview,
    clean_text
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Explore Netflix titles"
    )
    parser.add_argument(
        "--input",
        default="data/messy_netflix_titles.csv",
        help="Path to the Netflix CSV file"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show debug messages"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S"
    )

    # Create a Path object from args.input.
    # Inside a try block, load that path using pd.read_csv().
    # Catch FileNotFoundError, log an ERROR message,
    # and exit with sys.exit(1).
    # Log an INFO message.
    input_path = Path(args.input)
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        logger.error(f"File not found: {input_path}")
        sys.exit(1)
    logger.info(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns")

    df_original = df.copy()

    show_overview(df)
    logger.info("Displayed DataFrame overview")
    
    before = df.shape[0]
    df = remove_duplicates(df)
    logger.info(f"Removed {before - df.shape[0]} duplicate row(s)")

    before = df.shape[0]
    df = drop_missing_rows(df)
    logger.info(f"Dropped {before - df.shape[0]} rows with missing values")

    # TODO 3: wrap remove_iqr_outliers(df, "runtime_minutes", 1.5) in try/except ValueError -> sys.exit(1)
    # remember to track before/after count and log "Removed X runtime_minutes outlier(s)"
    try:
        before = df.shape[0]
        df = remove_iqr_outliers(df, "runtime_minutes", 1.5)
        after = df.shape[0]
        removed_count = before - after
        logger.debug(f"Removed IQR outliers from column '{column}': lower_bound={lower_bound}, upper_bound={upper_bound}, rows_removed={before - after}")
    except ValueError as e:
        logger.error(f"Error removing IQR outliers: {e}")
        sys.exit(1)

    # TODO 4: for column in ["title", "type", "country"]:
    #   apply clean_text, then logger.info(f"Cleaned text column: {column}")
    for column in ["title", "type", "country"]:
        df[column] = df[column].apply(clean_text)
        logger.info(f"Cleaned text column: {column}")

    # TODO 5: build report dict with rows_before (len(df_original)), rows_after (len(df)),
    #   rows_removed, columns (df.shape[1]) and log it
    report = {
        "rows_before": len(df_original),
        "rows_after": len(df),
        "rows_removed": len(df_original) - len(df),
        "columns": df.shape[1]
    }
    logger.info(f"Cleaning complete: {report}")

if __name__ == "__main__":
    main()
