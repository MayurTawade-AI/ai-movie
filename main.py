from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI , Depends , HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float, false
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker , Session
from Schemas import MovieCreate , MovieResponse
from ai_service import generate_movie_summary
from typing import Optional
DATABASE_URL = "sqlite:///./movies_V2.db"
engine = create_engine(DATABASE_URL , connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit = False , autoflush= False , bind= engine)
Base = declarative_base()

class MovieModel(Base):
    __tablename__ = "movies"
    id = Column(Integer , primary_key= True , index= True)
    title = Column(String)
    director = Column(String)
    rating = Column(Float)
    year = Column(Integer , nullable= True)
    summary = Column(String , nullable = True)
    tags = Column(String)

Base.metadata.create_all(bind= engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield  db
    finally:
        db.close()


@app.post("/movies" , response_model = MovieResponse)
def create_movie(movie: MovieCreate , db: Session = Depends(get_db)):
    ai_data = generate_movie_summary(movie.title, movie.director)
    ai_text_only = ai_data["summary"]
    if not movie.summary:
        final_summary = ai_text_only
    else:
        final_summary = movie.summary

    new_movie = MovieModel(
        title = movie.title,
        director = movie.director,
        rating = movie.rating,
        year = movie.year,
        summary = final_summary,
        tags = ai_data["tags"]
    )

    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie

@app.get("/movies" , response_model = list[MovieResponse])
def get_movies(tag: Optional[str] = None,db: Session = Depends(get_db)):
    if tag:
        movies = db.query(MovieModel).filter(MovieModel.tags.contains(tag)).all()
    else:
        movies = db.query(MovieModel).all()
    return movies

@app.get("/movies/{movie_id}" , response_model = MovieResponse)
def get_movies(movie_id : int , db:Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if movie is None :
        raise HTTPException(status_code= 404 , detail = "movie not found")
    return movie