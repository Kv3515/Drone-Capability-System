from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create the base class for declarative models
Base = declarative_base()

# Database URL for SQLite
DATABASE_URL = "sqlite:///drones.db"

# Create the engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Drone(Base):
    """
    SQLAlchemy model for the drones table.
    """
    __tablename__ = "drones"

    id = Column(Integer, primary_key=True, index=True)
    drone_name = Column(String, index=True)
    drone_class = Column(String)
    base_endurance = Column(Float)
    battery_health = Column(Float)
    reliability = Column(Float)
    total_drones = Column(Integer)
    mission_capable = Column(Integer)
    battery_sets = Column(Integer)


def init_db():
    """
    Initialize the database by creating all tables if they do not exist.
    """
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully. Table 'drones' created.")


def get_db():
    """
    Get a database session for use in queries.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
