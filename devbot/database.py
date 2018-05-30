"""
Python representation of the database for use with SQLAlchemy
"""
import os
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import dotenv

# Load environment variables using dotenv.
dotenv.load_dotenv(".env")

# Set database URL or use SQLite if none is given
db_url = (
    os.environ.get("DATABASE")
    if os.environ.get("DATABASE")
    else "sqlite:///database.sqlite"
)

SQLAlchemyBase = declarative_base()
engine = sa.create_engine(db_url, echo=False)
Session = sessionmaker(bind=engine)


class User(SQLAlchemyBase):
    __tablename__ = "user"
    # https://discordapp.com/developers/docs/resources/user
    id = sa.Column(sa.String(32), primary_key=True)
    username = sa.Column(sa.String(32))
    discriminator = sa.Column(sa.String(4))
    avatar = sa.Column(sa.String(32))
    bot = sa.Column(sa.Boolean)
    mfa_enabled = sa.Column(sa.Boolean)
    verified = sa.Column(sa.Boolean)
    email = sa.Column(sa.String(32))


class XKCD(SQLAlchemyBase):
    __tablename__ = "xkcd"
    # https://xkcd.com/info.0.json
    num = sa.Column(sa.Integer(), primary_key=True)
    img = sa.Column(sa.String(64))
    title = sa.Column(sa.String(32))
    safe_title = sa.Column(sa.String(32))
    alt = sa.Column(sa.String(256))
    transcript = sa.Column(sa.String(32))
    link = sa.Column(sa.String(32))
    news = sa.Column(sa.String(32))
    day = sa.Column(sa.String(2))
    month = sa.Column(sa.String(2))
    year = sa.Column(sa.String(4))


SQLAlchemyBase.metadata.create_all(engine)
