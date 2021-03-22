from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy.sql.expression import null


class qustFormBase(BaseModel):
    username:   str
    email:      str
    gender:     str
    height:     str
    weight:     str
    target:     str
    age_range:  str
    work_type:  str
    dining:     str
    cuisine:    str
    cook_tool:  Optional[str]
    cook_time:  str
    allergy:    Optional[str]

class qustFormCreate(qustFormBase):

    class Config:
        schema_extra = {
            "example": {
                "username": "Jack",
                "email":    "jack@gmal.com",
                "gender":   "男性",
                "height":   "161～170cm",
                "weight":   "61～65kg",
                "target":   "減重",
                "age_range":    "56歲以上",
                "work_type":    "輕度",
                "dining":       "出去吃",
                "cuisine":      "日韓",
                "cook_tool":    "電鍋",
                "cook_time":    "20",
                "allergy":      "麩質,甲殼"
            }
        }

class qustForm(qustFormBase):
    id:         int

    class Config:
        orm_mode = True
