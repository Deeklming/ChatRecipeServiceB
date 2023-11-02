from fastapi import APIRouter, HTTPException, status, Depends
from auth.hash_password import HashPassword
# from sqlmodel import select

from models.users import Users, SignIn


users_router = APIRouter(
    tags=["Users"],
)
users = {} # debug
hash_pw = HashPassword()


@users_router.post("/signup")
async def sign_up(new: Users) -> dict:
    if new.email in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied username exists."
        )
    users[new.email] = new
    return {
        "message": "User successfully registered!"
    }

@users_router.post("/signin")
async def sign_in(user: SignIn) -> dict:
    if user.email not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist."
        )
    if user.token == None:
        if users[user.email].password != user.password:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Wrong credentials passed."
            )
    else:
        if users[user.email].token != user.token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Wrong credentials passed."
            )

    return {
        "message": "User signed in successfully."
    }







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
