import logging
import re 
import pandas as pd

logger = logging.getLogger(__name__)


def show_overview(df):
    """Display basic information about a DataFrame."""
    # Log a DEBUG message containing the shape.
    # Print the shape, first five rows, column names, and data types.
    logger.debug(f"DataFrame shape: {df.shape}")
    print(df.head())
    print(list(df.columns))
    print(df.dtypes)


def remove_duplicates(df):
    """Remove exact duplicate rows."""
    # Remove exact duplicate rows.
    # Log a DEBUG message containing the before and after row counts.
    # Return the resulting DataFrame.
    before_count = df.shape[0]
    df = df.drop_duplicates()
    after_count = df.shape[0]
    logger.debug(f"Removed duplicates: before={before_count}, after={after_count}")
    return df


def drop_missing_rows(df):
    """Remove rows containing missing values."""
    # Drop rows containing one or more missing values.
    # Log a DEBUG message containing the before and after row counts.
    # Return the resulting DataFrame.
    before_count = df.shape[0]
    df = df.dropna()
    after_count = df.shape[0]
    logger.debug(f"Dropped missing rows: before={before_count}, after={after_count}")
    return df

def clean_text(value):
    """Normalize one text value."""
    # Strip surrounding whitespace.
    # Convert text to lowercase.
    # Collapse repeated whitespace.
    value = value.strip()
    value = value.lower()
    value = re.sub(r'\s+', ' ', value)
    return value


def remove_iqr_outliers(df, column, threshold):
    """Remove IQR outliers from one column."""
    # TODO 2:
    # If column does not exist:
    # Log an ERROR message and raise ValueError.
    # Calculate Q1, Q3, and IQR.
    # Use threshold to calculate lower and upper bounds.
    # Keep rows inside the bounds.
    # Log a DEBUG message containing the bounds and the number of rows removed.
    # Return the resulting DataFrame.
    if column not in df.columns:
        logger.error(f"Column '{column}' does not exist in DataFrame.")
        raise ValueError(f"Column '{column}' does not exist in DataFrame.")
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR
    df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    logger.debug(f"Removed IQR outliers from column '{column}': lower_bound={lower_bound}, upper_bound={upper_bound}")
    return df
