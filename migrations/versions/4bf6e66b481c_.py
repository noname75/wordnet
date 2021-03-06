"""empty message

Revision ID: 4bf6e66b481c
Revises: 
Create Date: 2017-06-08 19:41:06.338342

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4bf6e66b481c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('graph',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('source', sa.Enum('tags', 'responses'), nullable=True),
                    sa.Column('startTime', sa.DateTime(), nullable=True),
                    sa.Column('finishTime', sa.DateTime(), nullable=True),
                    sa.Column('minUserOnNode', sa.Integer(), nullable=True),
                    sa.Column('minUserOnEdge', sa.Integer(), nullable=True),
                    sa.Column('isDirected', sa.Boolean(), nullable=True),
                    sa.Column('minEdgeWeight', sa.Float(), nullable=True),
                    sa.Column('name', sa.Unicode(length=50), nullable=True),
                    sa.Column('moreInfo', sa.Unicode(length=150), nullable=True),
                    sa.Column('creationTime', sa.DateTime(), nullable=True),
                    sa.Column('isActive', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('phrase',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('content', sa.Unicode(length=200), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('content')
    )
    op.create_table('questionnaire',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('subject', sa.Unicode(length=100), nullable=True),
                    sa.Column('picture', sa.VARBINARY(), nullable=True),
                    sa.Column('moreInfo', sa.Unicode(length=1000), nullable=True),
                    sa.Column('isActive', sa.Boolean(), nullable=True),
                    sa.Column('isPictorial', sa.Boolean(), nullable=True),
                    sa.Column('creationTime', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('subject')
    )
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.Unicode(length=100), nullable=True),
                    sa.Column('password', sa.Unicode(length=60), nullable=True),
                    sa.Column('role', sa.Enum('admin', 'user'), nullable=True),
                    sa.Column('firstname', sa.Unicode(length=100), nullable=True),
                    sa.Column('lastname', sa.Unicode(length=100), nullable=True),
                    sa.Column('email', sa.Unicode(length=200), nullable=True),
                    sa.Column('moreinfo', sa.Unicode(length=1000), nullable=True),
                    sa.Column('bdate', sa.Date(), nullable=True),
                    sa.Column('gender', sa.Enum('زن', 'مرد'), nullable=True),
                    sa.Column('degree', sa.Enum('کارشناسی ارشد و دکتری', 'کارشناسی', 'فوق دیپلم', 'دیپلم', 'زیر دیپلم'),
                              nullable=True),
                    sa.Column('nativeLanguage', sa.Enum('فارسی', 'سایر زبان\u200cها'), nullable=True),
                    sa.Column('major', sa.Unicode(length=100), nullable=True),
                    sa.Column('registerationTime', sa.DateTime(), nullable=True),
                    sa.Column('isSeeGraphPage', sa.Boolean(), nullable=True),
                    sa.Column('isSeePackPage', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('username')
    )
    op.create_table('_edge_in_graph',
                    sa.Column('weight', sa.Float(), nullable=True),
                    sa.Column('phrase1_id', sa.Integer(), nullable=False),
                    sa.Column('phrase2_id', sa.Integer(), nullable=False),
                    sa.Column('graph_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['graph_id'], ['graph.id'], ),
                    sa.ForeignKeyConstraint(['phrase1_id'], ['phrase.id'], ),
                    sa.ForeignKeyConstraint(['phrase2_id'], ['phrase.id'], ),
                    sa.PrimaryKeyConstraint('phrase1_id', 'phrase2_id', 'graph_id')
    )
    op.create_table('_node_in_graph',
                    sa.Column('weight', sa.Float(), nullable=True),
                    sa.Column('phrase_id', sa.Integer(), nullable=False),
                    sa.Column('graph_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['graph_id'], ['graph.id'], ),
                    sa.ForeignKeyConstraint(['phrase_id'], ['phrase.id'], ),
                    sa.PrimaryKeyConstraint('phrase_id', 'graph_id')
    )
    op.create_table('_phrase_controller',
                    sa.Column('phrase_id', sa.Integer(), nullable=False),
                    sa.Column('credit', sa.Integer(), nullable=True),
                    sa.Column('type', sa.Enum('white', 'black'), nullable=True),
                    sa.ForeignKeyConstraint(['phrase_id'], ['phrase.id'], ),
                    sa.PrimaryKeyConstraint('phrase_id')
    )
    op.create_table('_phrase_in_questionnaire',
                    sa.Column('questionnaire_id', sa.Integer(), nullable=False),
                    sa.Column('phrase_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['phrase_id'], ['phrase.id'], ),
                    sa.ForeignKeyConstraint(['questionnaire_id'], ['questionnaire.id'], ),
                    sa.PrimaryKeyConstraint('questionnaire_id', 'phrase_id')
    )
    op.create_table('_picture_for_phrase',
                    sa.Column('phrase_id', sa.Integer(), nullable=False),
                    sa.Column('questionnaire_id', sa.Integer(), nullable=False),
                    sa.Column('picture', sa.VARBINARY(), nullable=False),
                    sa.ForeignKeyConstraint(['phrase_id'], ['phrase.id'], ),
                    sa.ForeignKeyConstraint(['questionnaire_id'], ['questionnaire.id'], ),
                    sa.PrimaryKeyConstraint('phrase_id', 'questionnaire_id')
    )
    op.create_table('_searched_phrase',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('phrase_id', sa.Integer(), nullable=False),
                    sa.Column('time', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['phrase_id'], ['phrase.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('user_id', 'phrase_id')
    )
    op.create_table('pack',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('startTime', sa.DateTime(), nullable=False),
                    sa.Column('finishTime', sa.DateTime(), nullable=True),
                    sa.Column('isPictorial', sa.Boolean(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('questionnaire_id', sa.Integer(), nullable=False),
                    sa.Column('isChecked', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(['questionnaire_id'], ['questionnaire.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('code', sa.Unicode(length=50), nullable=True),
                    sa.Column('caption', sa.Unicode(length=2500), nullable=False),
                    sa.Column('publishTime', sa.DateTime(), nullable=True),
                    sa.Column('storeTime', sa.DateTime(), nullable=True),
                    sa.Column('uid', sa.Integer(), nullable=True),
                    sa.Column('phrase_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['phrase_id'], ['phrase.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('code')
    )
    op.create_table('_response_in_pack',
                    sa.Column('duration', sa.Float(), nullable=True),
                    sa.Column('number', sa.Integer(), nullable=False),
                    sa.Column('phrase1_id', sa.Integer(), nullable=False),
                    sa.Column('phrase2_id', sa.Integer(), nullable=True),
                    sa.Column('pack_id', sa.Integer(), nullable=False),
                    sa.Column('creationTime', sa.DateTime(), nullable=True),
                    sa.Column('status', sa.Enum('accepted', 'rejected'), nullable=True),
                    sa.ForeignKeyConstraint(['pack_id'], ['pack.id'], ),
                    sa.ForeignKeyConstraint(['phrase1_id'], ['phrase.id'], ),
                    sa.ForeignKeyConstraint(['phrase2_id'], ['phrase.id'], ),
                    sa.PrimaryKeyConstraint('number', 'phrase1_id', 'pack_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_response_in_pack')
    op.drop_table('post')
    op.drop_table('pack')
    op.drop_table('_searched_phrase')
    op.drop_table('_picture_for_phrase')
    op.drop_table('_phrase_in_questionnaire')
    op.drop_table('_phrase_controller')
    op.drop_table('_node_in_graph')
    op.drop_table('_edge_in_graph')
    op.drop_table('user')
    op.drop_table('questionnaire')
    op.drop_table('phrase')
    op.drop_table('graph')
    # ### end Alembic commands ###
