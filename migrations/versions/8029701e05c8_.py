"""empty message

Revision ID: 8029701e05c8
Revises: 
Create Date: 2017-05-19 18:54:13.918609

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8029701e05c8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dictionary',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.Unicode(length=100), nullable=True),
                    sa.Column('language', sa.Enum('فارسی', 'انگلیسی', 'عربی', 'سایر زبان\u200cها'), nullable=True),
                    sa.Column('moreInfo', sa.Unicode(length=1000), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
    )
    op.create_table('graph',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('isDirect', sa.Boolean(), nullable=True),
                    sa.Column('isActive', sa.Boolean(), nullable=True),
                    sa.Column('language', sa.Enum('فارسی', 'انگلیسی', 'عربی', 'همه\u200cی زبان\u200cها'),
                              nullable=True),
                    sa.Column('source', sa.Enum('پاسخ\u200cهای کاربران سایت', 'تگ\u200cهای اینستاگرام',
                                                'تگ\u200cهای اینستاگرام و پاسخ\u200cهای کاربران سایت'), nullable=True),
                    sa.Column('minWeight', sa.Float(), nullable=True),
                    sa.Column('minFrequency', sa.Float(), nullable=True),
                    sa.Column('startTime', sa.DateTime(), nullable=True),
                    sa.Column('finishTime', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('picture',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.Unicode(length=200), nullable=True),
                    sa.Column('filePath', sa.Unicode(length=500), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
    )
    op.create_table('post',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('code', sa.Unicode(length=50), nullable=True),
                    sa.Column('publishTime', sa.DateTime(), nullable=True),
                    sa.Column('storeTime', sa.DateTime(), nullable=True),
                    sa.Column('uid', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('code')
    )
    op.create_table('questionnaire',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('subject', sa.Unicode(length=100), nullable=True),
                    sa.Column('isActive', sa.Boolean(), nullable=True),
                    sa.Column('isPictorial', sa.Boolean(), nullable=True),
                    sa.Column('isChosen', sa.Boolean(), nullable=True),
                    sa.Column('moreInfo', sa.Unicode(length=1000), nullable=True),
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
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('username')
    )
    op.create_table('pack',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('startTime', sa.DateTime(), nullable=True),
                    sa.Column('finishTime', sa.DateTime(), nullable=True),
                    sa.Column('isPictorial', sa.Boolean(), nullable=True),
                    sa.Column('isChosen', sa.Boolean(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('questionnaire_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['questionnaire_id'], ['questionnaire.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('phrase',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('content', sa.Unicode(length=200), nullable=True),
                    sa.Column('picture_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['picture_id'], ['picture.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('content')
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
    op.create_table('_phrase_in_dictionary',
                    sa.Column('dictionary_id', sa.Integer(), nullable=False),
                    sa.Column('phrase_id', sa.Integer(), nullable=False),
                    sa.Column('weight', sa.Float(), nullable=True),
                    sa.ForeignKeyConstraint(['dictionary_id'], ['dictionary.id'], ),
                    sa.ForeignKeyConstraint(['phrase_id'], ['phrase.id'], ),
                    sa.PrimaryKeyConstraint('dictionary_id', 'phrase_id')
    )
    op.create_table('_phrase_in_questionnaire',
                    sa.Column('questionnaire_id', sa.Integer(), nullable=False),
                    sa.Column('phrase_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['phrase_id'], ['phrase.id'], ),
                    sa.ForeignKeyConstraint(['questionnaire_id'], ['questionnaire.id'], ),
                    sa.PrimaryKeyConstraint('questionnaire_id', 'phrase_id')
    )
    op.create_table('_possible_response',
                    sa.Column('phrase1_id', sa.Integer(), nullable=False),
                    sa.Column('phrase2_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['phrase1_id'], ['phrase.id'], ),
                    sa.ForeignKeyConstraint(['phrase2_id'], ['phrase.id'], ),
                    sa.PrimaryKeyConstraint('phrase1_id', 'phrase2_id')
    )
    op.create_table('_response_in_pack',
                    sa.Column('duration', sa.Float(), nullable=True),
                    sa.Column('number', sa.Integer(), nullable=False),
                    sa.Column('phrase1_id', sa.Integer(), nullable=False),
                    sa.Column('phrase2_id', sa.Integer(), nullable=True),
                    sa.Column('pack_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['pack_id'], ['pack.id'], ),
                    sa.ForeignKeyConstraint(['phrase1_id'], ['phrase.id'], ),
                    sa.ForeignKeyConstraint(['phrase2_id'], ['phrase.id'], ),
                    sa.PrimaryKeyConstraint('number', 'phrase1_id', 'pack_id')
    )
    op.create_table('_searched_phrase',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('phrase_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['phrase_id'], ['phrase.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('user_id', 'phrase_id')
    )
    op.create_table('tag',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('frequency', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['id'], ['phrase.id'], ),
                    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('_tag_in_post',
                    sa.Column('number', sa.Integer(), nullable=True),
                    sa.Column('tag_id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
                    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
                    sa.PrimaryKeyConstraint('tag_id', 'post_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_tag_in_post')
    op.drop_table('tag')
    op.drop_table('_searched_phrase')
    op.drop_table('_response_in_pack')
    op.drop_table('_possible_response')
    op.drop_table('_phrase_in_questionnaire')
    op.drop_table('_phrase_in_dictionary')
    op.drop_table('_node_in_graph')
    op.drop_table('_edge_in_graph')
    op.drop_table('phrase')
    op.drop_table('pack')
    op.drop_table('user')
    op.drop_table('questionnaire')
    op.drop_table('post')
    op.drop_table('picture')
    op.drop_table('graph')
    op.drop_table('dictionary')
    # ### end Alembic commands ###
