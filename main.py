from fastapi import FastAPI, HTTPException
import psycopg2
import pandas as pd

# create FastAPI object
app = FastAPI()


def getConnection():
    # create connection
    conn = psycopg2.connect(
        dbname="neondb", user="neondb_owner", password="npg_sLfVg8iW4EwO",
        host="ep-steep-water-a102fmjl-pooler.ap-southeast-1.aws.neon.tech",
    )

    return conn

# bikin endpoint
@app.get('/')
async def getWelcome(): # function handler
    return {
        "msg": "sample-fastapi-pg"
    }


# endpoint untuk ngambil data profile
@app.get('/profiles')
async def getProfiles():
    # connect ke db
   conn = getConnection() # hasil getConnection itu object, save ke suatu var

   # pandas
   df = pd.read_sql("SELECT * FROM profiles", conn)

   # kasih response
   return df.to_dict(orient = 'records')


# endpoint untuk ngambil profile with filter
@app.get('/profiles/{id}')
async def getProfileById(id: int):
    # connect ke db
   conn = getConnection()

   # pandas
   df = pd.read_sql(f"SELECT * FROM profiles WHERE id = {id}", conn)

   # cek jika data nya kosong -> default yang sekarang list kosong [], status code nya 200 -> success
   # status code nya bener, tapi data nya ga ada, gabisa nampilin apa2
   # karena ga ada, harusnya error, kita harus bikin status code nya 404, kalau kosong
   if len(df) == 0:
       raise HTTPException(status_code=404, detail="Data tidak ditemukan!")


   # jika lengkap kasih response 200
   return df.to_dict(orient = 'records')


# @app.post(...)
# async def createProfile():
#     pass


# @app.patch(...)
# async def updateProfile():
#     pass


# @app.delete(...)
# async def deleteProfile():
#     pass
