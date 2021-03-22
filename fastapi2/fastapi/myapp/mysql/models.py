from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import VARCHAR

from .database import Base

## 模型 (model) 定義
class qustForm(Base):
    # 重新命名
    __tablename__ = 'qustForm'
    id        = Column(Integer, primary_key=True)
    username  = Column(VARCHAR(30), nullable=False)
    email     = Column(VARCHAR(30), unique=True, index=True, nullable=False)
    gender    = Column(VARCHAR(30), nullable=False)
    height    = Column(VARCHAR(30), nullable=False)
    weight    = Column(VARCHAR(30), nullable=False)
    target    = Column(VARCHAR(30), nullable=False)
    age_range = Column(VARCHAR(30), nullable=False)
    work_type = Column(VARCHAR(30), nullable=False)
    dining    = Column(VARCHAR(30), nullable=False)
    cuisine   = Column(VARCHAR(30), nullable=False)
    cook_tool = Column(VARCHAR(30), nullable=False)
    cook_time = Column(VARCHAR(30), nullable=False)
    allergy   = Column(VARCHAR(30), nullable=True)

    # def __init__(self, argv*):
    #     self.
    #     for i 
    #     # self.姓名 = name
    #     # self.性別 = sex
    #     # self.身高 = high
    #     # self.目標 = target
    #     # self.Id = 1
    #     self.name = name
    #     self.信箱 = sex
    #     self.性別 = high
    #     self.身高 = target
    #     self.體重 = a1
    #     self.目標 = a2
    #     self.年齡 = a3
    #     self.工作類型 = a4
    #     self.吃飯問題 = a5
    #     self.喜歡菜系 = a6
    #     self.廚房電器 = a7
    #     self.烹飪時間 = a8
    #     self.過敏類別 = a9

