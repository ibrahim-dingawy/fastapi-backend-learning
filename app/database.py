from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import DATABASE_URL


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()





"""
CLASSIC STYLE                MODERN 2.x STYLE

declarative_base()           DeclarativeBase

Column(Integer)              Mapped[int] + mapped_column()

Column(String)               Mapped[str] + mapped_column()

relationship(...)            Mapped[...] = relationship(...)

db.query(Video)              select(Video)

.filter(...)                 .where(...)

db.query(...).all()          db.scalars(select(...)).all()

Query by PK manually         db.get(Video, id)

add/commit/refresh            نفس الفكرة ✅
delete/commit                 نفس الفكرة ✅


الخطوة العملية دلوقتي: نعدّل database.py + models/user.py + models/video.py للـ Modern Mapping، وبعدها نعدل get_all_videos_orm, get_video_orm, وsearch_videos_orm ونشغل كل الـ pytest suite. لو كلها Passed، يبقى عملنا migration للكود نفسه من classic ORM style للـ modern 2.x style من غير ما نمس الـ database schema.

"""