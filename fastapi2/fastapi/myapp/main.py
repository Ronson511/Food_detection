## import fastapi related module/package
import uvicorn
from fastapi import FastAPI

from mysql.rt_qform       import router as r4_qustForm
from mylinebot.rt_linebot import router as r4_linebot
from mylinebot.rt_images  import router as r4_images

# create FastAPI server
app = FastAPI()

app.include_router(r4_qustForm, tags=["qustForm"],  prefix="/qustForm")
app.include_router(r4_linebot,  tags=["linebot01"], prefix="/linebot01")
app.include_router(r4_images,   tags=["images"],    prefix="/images")

# run app
if __name__ == "__main__":
    # if run from 'python main.py'
    uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=True)
    # from shell 'uvicorn main:app --host=127.0.0.1 --port=5000'

