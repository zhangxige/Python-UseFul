import unittest
from typing import List
from typing import Optional

from sqlalchemy import create_engine, String, ForeignKey, inspect
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

    def _reconnectdb(self):
        self._engine = create_engine(self._database, echo=True)

    # 初始化创建所有表
    def Create_Tables(self, tablebase: DeclarativeBase):
        tablebase.metadata.create_all(self._engine)
        self._reconnectdb()

    # 查询数据库中有哪些表
    def Inquery_DetailsTables(self):
        inspector = inspect(self._engine)
        instbls = inspector.get_table_names()
        return instbls

    # 删除表
    def Drop_Table(self, tablename: DeclarativeBase):
        tablename.metadata.drop_all(self._engine)
        self._reconnectdb()

    # 增
    def Insert_Data(self, insert_value):
        with self._session() as session:
            session.add(insert_value)
            session.commit()

    # 删
    def Delet_Data(self, table_name: DeclarativeBase, condition: dict):
        with self._session() as session:
            res = session.query(table_name).filter_by(**condition)
            res.delete()
            session.commit()

    # 改
    def Update_Data(self, tabel_name: DeclarativeBase, filter_cond: dict, new_v: dict):
        with self._session() as session:
            session.query(tabel_name).filter_by(**filter_cond).update(new_v)
            session.commit()

    # 查
    def Inquire_Data(self, table_name: DeclarativeBase):
        res = None
        with self._session() as session:
            res = session.query(table_name)
            for l_info in res:
                print(l_info)
        return res


# 单元测试
class TestSqlalchemy_Manager(unittest.TestCase):
    # preparation init test
    def setUp(self):
        # 每一个测试前都会执行
        print('test begin!')
        self.db_api = Sqlalchemy_Manager()

    def tearDown(self):
        # 每一个测试后都会执行
        print('end test!')

    def test_createtable(self):
        self.db_api.Create_Tables(BaseSoftWare)

    def test_drop_and_query_table(self):
        self.db_api.Create_Tables(Base)
        r = self.db_api.Inquery_DetailsTables()
        print(r)
        self.db_api.Drop_Table(Address)
        r = self.db_api.Inquery_DetailsTables()
        print(r)

    def test_insertdata(self):
        testdata1 = SoftWare(
            name='softwarename1',
            fullname='fullname1',
            version='1.0',
            address='qwzw'
            )
        testdata2 = UsedSence(email_address='address1')
        self.db_api.Insert_Data(testdata1)
        self.db_api.Insert_Data(testdata2)

    def test_updatedata(self):
        filter_cond = {'name': 'softwarename1'}
        update_dict = {
            SoftWare.fullname: 'new_name',
            SoftWare.version: '2.0'
        }
        self.db_api.Update_Data(SoftWare, filter_cond, update_dict)

    def test_deletedata(self):
        filter_cond = {'name': 'softwarename1'}
        self.db_api.Delet_Data(SoftWare, filter_cond)

    def test_querydata(self):
        self.db_api.Inquire_Data(UsedSence)
        self.db_api.Inquire_Data(SoftWare)


if __name__ == "__main__":
    unittest.main()
