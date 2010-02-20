"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

from nitrol.model import meta

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    meta.Session.configure(bind=engine)
    meta.engine = engine

players_table = sa.Table("players", meta.metadata,
        sa.Column("id", sa.types.Integer, sa.schema.Sequence('players_seq_id', optional = True), primary_key=True),
        sa.Column("first_name", sa.types.String(32), nullable=False),
        sa.Column("last_name", sa.types.String(32), nullable=False),
        # sa.Column("email", sa.types.String(128), nullable=False),
        sa.Column("rank_num", sa.types.Integer, nullable=False),
        sa.Column("dan", sa.types.Boolean, nullable=False),
        sa.Column("egf", sa.types.Integer, nullable=True),
        )

class Player(object):
    def get_rank(self):
        return self.rank_num + 'd' if self.dan else 'k'
    def set_rank(self, rank):
        self.rank_num = rank[:-1]
        self.dan = rank[-1] is 'd'

    rank=property(get_rank, set_rank, None, "Rank in short form")

orm.mapper(Player, players_table)
