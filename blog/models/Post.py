from blog.models.db_config import *
from sqlalchemy import func, extract, distinct

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.Unicode(50), unique=True)
    caption = db.Column(db.Unicode(2500), nullable=False)
    publishTime = db.Column(db.DateTime)
    storeTime = db.Column(db.DateTime)
    uid = db.Column(db.Integer)
    phrase_id = db.Column(db.ForeignKey(Phrase.id))


    def __init__(self, code=None, caption=None, publishTime=None, storeTime=None, uid=None, phrase_id=None):
        self.code = code
        self.caption = caption
        self.publishTime = publishTime
        self.storeTime = storeTime
        self.uid = uid
        self.phrase_id = phrase_id


    def addPost(self):
        db.session.add(self)
        db.session.commit()

    def getPost_byCode(self):
        return db.session.query(Post).filter_by(code=self.code).first()


    def addIfNotExists(self):
        if not self.getPost_byCode():
            self.addPost()


    def getCountGroupByPhraseId(self):
        return db.session.query(
            Post.phrase_id,
            func.count(Post.phrase_id).label('count')
        ).group_by(Post.phrase_id).order_by('count DESC').all()


    def getCountGroupByTime(self):
        return db.session.query(
            extract('year', Post.publishTime).label('year'),
            extract('month', Post.publishTime).label('month'),
            func.count(Post.caption).label('count')
        ).group_by(
            extract('year', Post.publishTime),
            extract('month', Post.publishTime)
        ).order_by(
            extract('year', Post.publishTime),
            extract('month', Post.publishTime)
        ).all()


    def getCountGroupByUid(self):
        return db.session.query(func.count(Post.caption).label('count')).group_by(Post.uid).all()


    def getCountOfPosts(self):
        return db.session.query(func.count(Post.caption)).scalar()

    def getCountOfUids(self):
        return db.session.query(func.count(distinct(Post.uid))).scalar()

    def getCountOfPhrases(self):
        return db.session.query(func.count(distinct(Post.phrase_id))).scalar()

