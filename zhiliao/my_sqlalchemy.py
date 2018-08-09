
from sqlalchemy import Column,String,create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(String(20),primary_key=True)
    username = Column(String(20))

engine = create_engine('mysql+pymysql://root:123456@localhost:3306/sql_alchemy')
DBSession = sessionmaker(bind=engine)

User()
session = DBSession()
new_user = User(id='5', username='Bob')
# 添加到session:
session.add(new_user)
# 提交即保存到数据库:
session.commit()
# 关闭session:
session.close()