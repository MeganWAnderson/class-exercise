#main.py
import logging
import io
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, Query, File, UploadFile, HTTPException

from src import (
    ProcessConfig,
    MovieInput,
    MovieResponse,
    CSVInfo,
    DataStorage,
)
from middleware import log_requests

app = FastAPI(title="Movie API")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)
storage = DataStorage()

movies = {
    1: {"id": 1, "title": "Movie A", "release_year": 2020},
    2: {"id": 2, "title": "Movie B", "release_year": 2021},
}


@app.get("/health")
def health_check():
    return {"status": "ok"}


#a path parameter identifies a resource (movie) to retrieve
@app.get("/demo/movies/{movie_id}")
def demo_get_movie(movie_id: int): #type annotation: it declares the expected type, int
    return {"requested_id": movie_id}


from fastapi import Query

#a query parameter adjusts a request
@app.get("/demo/movies")
def demo_list_movies(limit: int = Query(default=2, ge=1)):
    #The default is 2 when limit is omitted in the query.
    # ge=1 means greater than or equal to one.
    return {"requested_limit": limit}


from src import MovieInput

@app.post("/demo/movies")
def demo_add_movie(movie: MovieInput):
    return movie.model_dump() #Converts the model to a Python dictionary.


from src import MovieResponse

demo_movie_examples = []

@app.post("/demo/movie-examples", response_model=MovieResponse)
def demo_add_movie_example(movie: MovieInput):
    movie_id = len(demo_movie_examples) + 1
    record = movie.model_dump()
    record["id"] = movie_id
    demo_movie_examples.append(record)
    return record

#main.py


@app.get("/movies", response_model=list[MovieResponse])
def list_movies(limit: int = Query(default=2, ge=1)):
    result = list(movies.values())[:limit]
    logger.info(f"Returning {len(result)} movies.")
    return result


@app.post("/movies", response_model=MovieResponse)
def add_movie(movie: MovieInput):
    movie_id = len(movies) + 1

    # Convert movie to a dictionary, add the new ID, and store it.
    record = movie.model_dump()
    record["id"] = movie_id
    movies[movie_id] = record

    # Log the new ID at INFO and return the stored record.
    logger.info("Added movie: id=%d", movie_id)
    return record

@app.post("/demo/process-config")
def demo_process_config(config: ProcessConfig):
    df = pd.DataFrame({"title": ["Movie A", "Movie A", "Movie B", None]})
    settings = config.model_dump()

    if settings["processing"]["remove_duplicates"]:
        df = df.drop_duplicates()

    if settings["processing"]["drop_missing"]:
        df = df.dropna()

    return {"rows": len(df)}

@app.post("/inspect-csv", response_model=CSVInfo)
async def inspect_csv(file: UploadFile = File(...)):
    # Check that the uploaded filename ends in .csv
    if Path(file.filename or "").suffix.lower() != ".csv":
        logger.warning("Rejected non-CSV file: %s", file.filename)
        raise HTTPException(
            status_code=400,
            detail="File must be a CSV",
        )

    # Read and parse the uploaded file
    contents = await file.read()

    try:
        df = pd.read_csv(io.BytesIO(contents))
    except (
        pd.errors.EmptyDataError,
        pd.errors.ParserError,
        UnicodeDecodeError,
    ) as error:
        logger.warning("Cannot read CSV: %s", error)
        raise HTTPException(
            status_code=400,
            detail="Cannot read the uploaded CSV",
        )

    # Store the dataset and assign its ID
    dataset_id = storage.save_data(df, file.filename)

    logger.info(
        "Stored CSV: id=%s, filename=%s",
        dataset_id,
        file.filename,
    )

    return CSVInfo(
        filename=file.filename,
        rows=len(df),
        columns=len(df.columns),
        column_names=list(df.columns),
        dataset_id=dataset_id,
    )

@app.get("/datasets/{dataset_id}/shape")
def get_dataset_shape(dataset_id: int):
    df = storage.get_data(dataset_id)

    if df is None:
        logger.warning("Dataset not found: %s", dataset_id)
        raise HTTPException(
            status_code=404,
            detail="Dataset not found",
        )

    logger.info("Retrieved dataset shape: id=%s", dataset_id)

    return {
        "dataset_id": dataset_id,
        "rows": len(df),
        "columns": len(df.columns),
    }

app.middleware("http")(log_requests)

