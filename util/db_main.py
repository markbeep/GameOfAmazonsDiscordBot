from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from models import User, MatchHistory, Base


conn_string = "sqlite:///data.db"
engine = create_engine(conn_string)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def add_user(user_id):
    new_user = User(discord_user_id=user_id)
    session.add(new_user)
    session.commit()


def add_match(player_1_id, player_2_id, winner_id):
    add_user(player_1_id)
    add_user(player_2_id)
    new_match = MatchHistory(player_1_id=player_1_id, player_2_id=player_2_id, winner_id=winner_id)
    session.add(new_match)
    session.commit()