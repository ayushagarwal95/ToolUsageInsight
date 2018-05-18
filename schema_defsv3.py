from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///toolusage.db', echo=True)
Base = declarative_base()

########################################################################


class sessiondata(Base):
    """"""
    __tablename__ = "sessiondata"

    xy = Column(Integer, primary_key=True)
    sessionid = Column(String, primary_key=True)
    toolid    = Column(Integer, primary_key=True)
    starttime = Column(String)
    endtime   = Column(String)
    duration  = Column(String)

    def __init__(self, xy,sessionid,toolid,starttime,endtime = None,duration = None):
        """"""
        self.xy = xy
        self.sessionid = sessionid
        self.toolid = toolid
        if starttime is not None:
            self.starttime = starttime
        self.endtime = endtime
        self.duration = duration


class users(Base):
    """"""
    __tablename__ = "users"

    userid   = Column(String, primary_key=True)
    password = Column(String)
    role    = Column(String)
    region   = Column(String)

    def __init__(self, userid, password,role,region):
        """"""
        self.userid = userid
        self.password = password
        self.role    = role
        self.region   = region


class usersession(Base):
    """"""
    __tablename__ = "usersession"

    id = Column(Integer, primary_key=True)
    userid    = Column(String)
    sessionid = Column(Integer)

    def __init__(self, userid, sessionid):
        """"""
        self.userid = userid
        self.sessionid = sessionid

class tooldata(Base):
    """"""
    __tablename__ = "tooldata"

    toolid    = Column(Integer, primary_key=True)
    toolname  = Column(String)
    tooltype  = Column(String)
    url       = Column(String)

    def __init__(self, toolid,toolname,tooltype, url = None):
        """"""
        self.toolid = toolid
        self.toolname= toolname
        self.tooltype = tooltype
        self.url = url


# create tables
Base.metadata.create_all(engine)


