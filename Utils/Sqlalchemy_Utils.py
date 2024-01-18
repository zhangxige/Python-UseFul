from typing import List
from typing import Optional

from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


# base calss
class Base(DeclarativeBase):
    pass


# user real information
class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return (f"""User(id={self.id!r},
                 name={self.name!r},
                 fullname={self.fullname!r})""")


# user internet information
class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


# create table
def Sqlalchemy_CreatTable():
    engine = create_engine('sqlite:///Player.db', echo=True)
    # 创建表
    Base.metadata.create_all(engine)


# insert data
def Sqlalchemy_Insert():
    engine = create_engine('sqlite:///Player.db', echo=True)
    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 添加数据
    ed_user = User(name='ed', fullname='Ed Jones')
    with session as session:
        session.add(ed_user)
        session.commit()

    # 添加多条记录
    with session as session:
        session.add_all([
            User(name='wendy', fullname='Wendy Williams'),
            User(name='mary', fullname='Mary Contrary'),
            User(name='fred', fullname='Fred Flinstone')
        ])
        session.commit()


# 删除
def Sqlalchemy_DeleteData():
    engine = create_engine('sqlite:///Player.db', echo=True)
    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 查询
    with session as session:
        res = session.query(User).filter_by(name='ed')
        for l_info in res:
            print(l_info)

    # 删除
    with session as session:
        res = session.query(User).filter_by(name='wendy')
        res.delete()
        session.commit()

    # 查询
    with session as session:
        res = session.query(User)
        for l_info in res:
            print(l_info)


# 查询
def Sqlalchemy_QueryData():
    engine = create_engine('sqlite:///Player.db', echo=False)
    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 查询
    with session as session:
        res = session.query(User)
        for l_info in res:
            print(l_info)


# 更新
def Sqlalchemy_UpdateData():
    engine = create_engine('sqlite:///Player.db', echo=True)
    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 更新
    with session as session:
        n = 'Paul C'
        session.query(User).filter_by(name='ed').update({User.fullname: n})
        session.commit()


if __name__ == "__main__":
    # Sqlalchemy_Insert()
    Sqlalchemy_UpdateData()
    Sqlalchemy_QueryData()
    # Sqlalchemy_DeleteData()
