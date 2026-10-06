import logging
import pandas as pd

logger = logging.getLogger(__name__)

def load_netflix(filepath):
    """Load the Netflix CSV file."""
    # TODO 1:
    # Load filepath using pd.read_csv().
    # Log an INFO.
    # Return the DataFrame.
    try:
        df = pd.read_csv(filepath)
        logger.info(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns from {filepath}")
        return df
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise

