from sqlalchemy import ForeignKey, Integer, Column
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "games"
    discord_user_id=Column("discord_user_id", Integer, primary_key=True)


class MatchHistory(Base):
    __tablename__ = "match_history"
    id=Column(Integer, primary_key=True)
    player_1_id=Column(Integer, ForeignKey("games.discord_user_id"))
    player_2_id=Column(Integer, ForeignKey("games.discord_user_id"))
    winner_id=Column(Integer, ForeignKey("games.discord_user_id"))
