from sqlalchemy import func, desc, and_, column
from blog.models.db_config import *


class ResponseInPack(db.Model):
    __tablename__ = '_response_in_pack'
    duration = db.Column(db.Float)
    number = db.Column(db.Integer, primary_key=True, default=1)
    phrase1_id = db.Column(db.ForeignKey(Phrase.id), primary_key=True)
    phrase2_id = db.Column(db.ForeignKey(Phrase.id))
    pack_id = db.Column(db.ForeignKey(Pack.id), primary_key=True)
    creationTime = db.Column(db.DateTime())
    status = db.Column(db.Enum('accepted', 'rejected'))


    def getResponseInPack(self):
        return db.session.query(ResponseInPack).filter_by(pack_id=self.pack_id,
                                                          phrase1_id=self.phrase1_id,
                                                          phrase2_id=self.phrase2_id).first()

    def getResponseList_byPackId(pack_id):
        return db.session.query(ResponseInPack).filter_by(pack_id=pack_id).all()

    def getResponseCount_byPackId(pack_id):
        return db.session.query(func.count(ResponseInPack.phrase1_id)).filter_by(pack_id=pack_id).filter(
            column('phrase2_id').isnot(None)).scalar()

    def getResponseCount_byPhraseId(phrase_id):
        return db.session.query(func.count(ResponseInPack.phrase2_id)).filter_by(phrase1_id=phrase_id).scalar()

    def getAcceptedResponses(self):
        return db.session.query(ResponseInPack).filter_by(status='accepted').filter(
            ResponseInPack.phrase2_id.isnot(None)).all()

    def getAcceptedResponseCount(self):
        return db.session.query(func.count(ResponseInPack.phrase2_id)).filter_by(status='accepted').scalar()

    def getAcceptedResponses_byStartTimeAndFinishTime(self, startTime, finishTime):
        return db.session.query(ResponseInPack).filter(ResponseInPack.phrase2_id.isnot(None),
                                                       ResponseInPack.creationTime >= startTime,
                                                       ResponseInPack.creationTime <= finishTime,
                                                       ResponseInPack.status == 'accepted').all()

    def getAcceptedResponseCount_byStartTimeAndFinishTime(self, startTime, finishTime):
        return db.session.query(func.count(ResponseInPack.phrase2_id)).filter(ResponseInPack.creationTime >= startTime,
                                                                              ResponseInPack.creationTime <= finishTime,
                                                                              ResponseInPack.status == 'accepted').scalar()

    def getAcceptedResponseCount_byStartTime(self, startTime):
        return db.session.query(func.count(ResponseInPack.phrase2_id)).filter(ResponseInPack.creationTime >= startTime,
                                                                              ResponseInPack.status == 'accepted').scalar()

    def __init__(self, pack_id=None, phrase1_id=None, phrase2_id=None, duration=None, creationTime=None, status=None):
        self.pack_id = pack_id
        self.phrase1_id = phrase1_id
        self.phrase2_id = phrase2_id
        self.duration = duration
        self.creationTime = creationTime
        self.status = status

    def addResponseInPack(self):
        lastSamePhrase1_id = db.session.query(ResponseInPack).filter_by(phrase1_id=self.phrase1_id,
                                                                        pack_id=self.pack_id).order_by(
            desc(ResponseInPack.number)).first()
        if lastSamePhrase1_id:
            if not lastSamePhrase1_id.duration:
                lastSamePhrase1_id.duration = self.duration
                lastSamePhrase1_id.phrase2_id = self.phrase2_id
            else:
                self.number = lastSamePhrase1_id.number + 1
                if not db.session.query(ResponseInPack).filter_by(pack_id=self.pack_id, phrase1_id=self.phrase1_id,
                                                                  phrase2_id=self.phrase2_id):
                    db.session.add(self)
        else:
            db.session.add(self)
        db.session.commit()

        return self


    def unansweredPhraseId(self):
        return db.session.query(ResponseInPack.phrase1_id).filter_by(pack_id=self.pack_id, duration=None).first()


    def setStatus(self, status):
        self.status = status
        db.session.commit()