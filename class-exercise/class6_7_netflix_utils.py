import logging

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
