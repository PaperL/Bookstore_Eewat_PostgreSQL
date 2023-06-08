import jwt
import time
import logging
from typing import Tuple

from psycopg2 import IntegrityError
from be.model import error
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

from be.model.database import getDatabaseBase, getDatabaseSession

# encode a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }


def jwt_encode(user_id: str, terminal: str) -> str:
    encoded = jwt.encode(
        {"user_id": user_id, "terminal": terminal, "timestamp": time.time()},
        key=user_id,
        algorithm="HS256",
    )
    return encoded.encode("utf-8").decode("utf-8")


# decode a JWT to a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }
def jwt_decode(encoded_token, user_id: str) -> str:
    decoded = jwt.decode(encoded_token, key=user_id, algorithms="HS256")
    return decoded


Base = getDatabaseBase()


class User(Base):
    __tablename__ = 'user'

    user_id = Column(String, primary_key=True)
    password = Column(String)
    balance = Column(Integer)
    token = Column(String)
    terminal = Column(String)

    token_lifetime: int = 3600  # 3600 seconds

    def __check_token(self, user_id, db_token, token) -> bool:
        try:
            if db_token != token:
                return False
            jwt_text = jwt_decode(encoded_token=token, user_id=user_id)
            ts = jwt_text["timestamp"]
            if ts is not None:
                now = time.time()
                if self.token_lifetime > now - ts >= 0:
                    return True
        except jwt.exceptions.InvalidSignatureError as e:
            logging.error(str(e))
            return False

    def register(self, user_id: str, password: str):
        try:
            session = getDatabaseSession()
            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)

            user = User(
                user_id=user_id,
                password=password,
                balance=0,
                token=token,
                terminal=terminal
            )

            session.add(user)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            return error.error_exist_user_id(user_id)
        return 200, "ok"

    def check_token(self, user_id: str, token: str) -> Tuple[int, str]:
        try:
            session = getDatabaseSession()
            user = session.query(User).filter_by(user_id=user_id).first()
            if user is None:
                return error.error_authorization_fail()
            db_token = user.token
            if not self.__check_token(user_id, db_token, token):
                return error.error_authorization_fail()
        except Exception as e:
            return 530, str(e)
        return 200, "ok"

    def check_password(self, user_id: str, password: str) -> Tuple[int, str]:
        try:
            session = getDatabaseSession()
            user = session.query(User).filter_by(user_id=user_id).first()
            if user is None:
                return error.error_authorization_fail()

            if password != user.password:
                return error.error_authorization_fail()

        except Exception as e:
            return 530, str(e)

        return 200, "ok"

    def login(self, user_id: str, password: str, terminal: str) -> Tuple[int, str, str]:
        token = ""
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message, ""

            token = jwt_encode(user_id, terminal)
            session = getDatabaseSession()
            user = session.query(User).filter_by(user_id=user_id).first()
            if user is None:
                return error.error_authorization_fail() + ("", )

            user.token = token
            user.terminal = terminal
            session.commit()

        except Exception as e:
            session.rollback()
            return 530, str(e), ""

        return 200, "ok", token

    def logout(self, user_id: str, token: str) -> bool:
        try:
            code, message = self.check_token(user_id, token)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            dummy_token = jwt_encode(user_id, terminal)

            session = getDatabaseSession()
            user = session.query(User).filter_by(user_id=user_id).first()
            if user is None:
                return error.error_authorization_fail()

            user.token = dummy_token
            user.terminal = terminal
            session.commit()
        except Exception as e:
            session.rollback()
            return 530, str(e)

        return 200, "ok"

    def unregister(self, user_id: str, password: str) -> Tuple[int, str]:
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message

            session = getDatabaseSession()
            user = session.query(User).filter_by(user_id=user_id).first()
            if user is None:
                return error.error_authorization_fail()

            session.delete(user)
            session.commit()

        except Exception as e:
            session.rollback()
            return 530, str(e)

        return 200, "ok"

    def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        try:
            code, message = self.check_password(user_id, old_password)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)

            session = getDatabaseSession()
            user = session.query(User).filter_by(user_id=user_id).first()
            if user is None:
                return error.error_authorization_fail()

            user.password = new_password
            user.token = token
            user.terminal = terminal
            session.commit()

        except Exception as e:
            session.rollback()
            return 530, str(e)

        return 200, "ok"
    
def getBalance(user_id: str) -> int:
    with getDatabaseSession() as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        if user:
            return user.balance
        return 0
