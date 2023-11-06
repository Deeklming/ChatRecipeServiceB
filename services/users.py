from fastapi import APIRouter, HTTPException, status, Depends, Response
from dbms.mariadb import dbaio
from models.users import User

users_router = APIRouter(
    tags=["User"],
)


@users_router.post('/create', status_code=status.HTTP_201_CREATED)
@dbaio
async def create_user(db, cur, user: User):
    pass



# @users_router.get('/all', status_code=status.HTTP_200_OK)
# async def get_all_users(db: Session = Depends(get_db)):
#     all_users = db.query(mU).all()
#     return all_users

# @users_router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
# async def delete_user(id: int, db: Session = Depends(get_db)):
#     delete_id = db.query(mU).filter(mU.id == id)
#     if delete_id == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User does not exist."
#         )
#     else:
#         delete_id.delete(synchronize_session=False)
#         db.commit()
#     return {"a":"b"}

# @users_router.put('/update/{id}', status_code=status.HTTP_200_OK)
# async def update_user(id: int, user: sU, db: Session = Depends(get_db)):
#     update_id = db.query(mU).filter(mU.id == id)
#     update_id.first()
#     if update_id == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User does not exist."
#         )
#     else:
#         update_id.update(user.dict(), synchronize_session=False)
#         db.commit()
#     return update_id.first()

# @users_router.post('/new', status_code=status.HTTP_201_CREATED)
# def create_user(new: Users, session = Depends(db.get_db)):
#     # new_note = Users(**payload.dict())
#     session.add(new)
#     session.commit()
#     session.refresh(new)
#     return {"status": "success", "message": new}



# @users_router.post("/signup")
# async def sign_up(new: Users) -> dict:
#     if new.email in users:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="User with supplied username exists."
#         )
#     users[new.email] = new
#     return {
#         "message": "User successfully registered!"
#     }

# @users_router.post("/signin")
# async def sign_in(user: SignIn) -> dict:
#     if user.email not in users:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User does not exist."
#         )
#     if user.token == None:
#         if users[user.email].password != user.password:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Wrong credentials passed."
#             )
#     else:
#         if users[user.email].token != user.token:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Wrong credentials passed."
#             )

#     return {
#         "message": "User signed in successfully."
#     }



# @user_router.post("/signup")
# async def sign_user_up(user: User, session=Depends(get_session)) -> dict:
    # print(f"user: {user}")
    # get_user = session.get(User, user.email)
    # statement = select(User)
    # print(f"get_user: {get_user}")
    # user_exist = True
    # if user_exist:
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail="User with supplied username exists."
    #     )
    # hashed_password = hash_password.create_hash(user.password)
    # user.password = hashed_password
    # session.add(user)
    # session.commit()
    # session.refresh(user)
    # return {
    #     "message": "User successfully registered!"
    # }
