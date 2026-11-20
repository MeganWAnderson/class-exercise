import logging
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, Query

from check_analysis import filter_movies, summarize_genres, summarize_years

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Movie Analysis API")
df = pd.read_csv(Path("data") / "class20_movies.csv")


@app.get("/analysis/genres", response_model=list[dict])
def get_genres(min_movies: int = Query(default=1, ge=1)):
    summary = summarize_genres(df, min_movies=min_movies)
    logger.info(f"Returning {len(summary)} genre groups with min_movies={min_movies}")
    return summary.to_dict(orient="records")

@app.get("/analysis/years", response_model=list[dict])
def get_years(window: int = Query(default=3, ge=1)):
    summary = summarize_years(df, window=window)
    logger.info(f"Returning {len(summary)} years with window={window}")
    return summary.to_dict(orient="records")

@app.get("/movies/filter", response_model=list[dict])
def get_filtered_movies(min_rating: float = Query(default=8.0, ge=0, le=10)):
    result = filter_movies(df, min_rating)
    records = result.to_dict(orient="records")
    logger.info(f"Filtered movies: rows={len(records)}, min_rating={min_rating}")
    return records