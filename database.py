import os, logging 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql.sqltypes import Float, Numeric


# see videos below for help:
# https://www.youtube.com/watch?v=jaKMm9njcJc&list=PL4iRawDSyRvVd1V7A45YtAGzDk6ljVPm1




SettingsBase = declarative_base()
class WidgetSettings(SettingsBase):
    __tablename__ = 'widget_settings'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    #other cols



class SettingsDb():

  def __init__(self) -> None:
    my_dir = os.path.dirname(__file__)
    main_dir = os.path.dirname(my_dir)
    engine = create_engine('sqlite:///'+ main_dir + "/settings/settings.db") #should create a .db file next to main.py
    self.models = {
        "widget_settings": WidgetSettings,
    }
    Session = sessionmaker(bind=engine)
    self.session = Session()
    SettingsBase.metadata.create_all(engine) #creates all the tables above

    def close(self):
      self.session.close()