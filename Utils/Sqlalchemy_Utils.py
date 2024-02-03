import pprint
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


# ============================  sepqrate ======================================


# software table base calss
class BaseSoftWare(DeclarativeBase):
    pass


# software basic infomation
class SoftWare(BaseSoftWare):
    __tablename__ = "Software_Info"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    version: Mapped[str] = mapped_column(String(30))
    address: Mapped[str] = mapped_column(String(30))
    addresses: Mapped[List["UsedSence"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return (f"""Software_Info(id={self.id!r},name={self.name!r},fullname={self.fullname!r}),version={self.version}""")


# software used sence
class UsedSence(BaseSoftWare):
    __tablename__ = "Used_Sence"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("Software_Info.id"))
    user: Mapped[SoftWare] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Used_Sence(id={self.id!r}, email_address={self.email_address!r})"


#  数据库管理类
class Sqlalchemy_Manager:
    def __init__(self, databese=r'sqlite:///Player.db') -> None:
        self._database = databese
        self._engine = create_engine(self._database, echo=True)
        # 创建会话
        self._session = sessionmaker(bind=self._engine)

    def __repr__(self) -> str:
        return f'mydatabase : {self._database}'

    # 初始化创建所有表
    def Create_Tables(self, tablebase: DeclarativeBase):
        tablebase.metadata.create_all(self._engine)

    # 增
    def Insert_Data(self, insert_value):
        with self._session() as session:
            session.add(insert_value)
            session.commit()

    # 删
    def Delet_Data(self, table_name, condition):
        with self._session() as session:
            res = session.query(table_name).filter_by(**condition)
            res.delete()
            session.commit()

    # 改
    def Update_Data(self, tabel_name, filter_cond: dict, new_v: dict):
        with self._session() as session:
            session.query(tabel_name).filter_by(**filter_cond).update(new_v)
            session.commit()

    # 查
    def Inquire_Data(self, table_name):
        res = None
        with self._session() as session:
            res = session.query(table_name)
            for l_info in res:
                print(l_info)
        return res


# test_case
def test_():
    db_api = Sqlalchemy_Manager()
    db_api.Create_Tables(BaseSoftWare)
    testdata1 = SoftWare(
        name='softwarename1',
        fullname='fullname1',
        version='1.0',
        address='qwzw'
        )
    testdata2 = UsedSence(email_address='address1')
    filter_cond = {'name': 'softwarename1'}
    update_dict = {SoftWare.fullname: 'new_name',
                   SoftWare.version: '2.0'}

    db_api.Insert_Data(testdata1)
    db_api.Inquire_Data(SoftWare)
    db_api.Update_Data(SoftWare, filter_cond, update_dict)
    db_api.Inquire_Data(SoftWare)


if __name__ == "__main__":
    # Sqlalchemy_CreatTable()
    # Sqlalchemy_Insert()
    # Sqlalchemy_UpdateData()
    # Sqlalchemy_QueryData()
    # Sqlalchemy_DeleteData()
    # Sqlalchemy_QueryData()
    test_()
