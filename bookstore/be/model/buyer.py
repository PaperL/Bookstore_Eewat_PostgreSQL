from typing import Tuple, List
from datetime import datetime
import uuid
import json
import logging
from sqlalchemy import Column, Integer, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from be.model.database import getDatabaseBase, getDatabaseSession
from be.model.user import User, getBalance
from be.model import error
from be.model.tables import NewOrder, NewOrderDetail, StoreBook, UserStore, store_id_exist


class Buyer():
    def __init__(self):
        self.paytimeLimit: int = 900  # 900s

    def new_order(self, user_id: str, token: str, store_id: str, id_and_count: List[Tuple[str, int]]) -> Tuple[int, str, str]:
        session = getDatabaseSession()
        try:
            user = session.query(User).filter(User.user_id == user_id).first()
            if not user:
                return error.error_non_exist_user_id(user_id) + (order_id,)
            if not store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id) + (order_id,)

            code, msg = user.check_token(user_id, token)
            if code != 200:
                return code, msg, ""

            order_id = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))

            total_price = 0
            for book_id, count in id_and_count:
                book = session.query(StoreBook).filter(
                    StoreBook.book_id == book_id,
                    StoreBook.store_id == store_id).first()
                if not book:
                    return error.error_non_exist_book_id(book_id) + (order_id,)

                stock_level = book.stock_level
                book_info = book.book_info
                book_info_json = json.loads(book_info)
                price = book_info_json.get("price")
                total_price += count * price
                print(stock_level, count)
                if stock_level < count:
                    return error.error_stock_level_low(book_id) + (order_id,)

                # DECREASE IN DELEVER_ORDER!!
                # book.stock_level -= count

                session.add(NewOrderDetail(order_id=order_id,
                            book_id=book_id, count=count, price=price))

            curTime = datetime.now()
            session.add(NewOrder(order_id=order_id, store_id=store_id, user_id=user_id,
                        order_time=curTime, total_price=total_price, paid=False, cancelled=False, delivered=False))
            session.commit()

        except Exception as e:
            print(e)
            session.close()
            logging.info("530, {}".format(str(e)))
            return 530, "{}".format(str(e)), ""
        finally:
            session.close()
        return 200, "ok", order_id

    def payment(self, user_id: str, password: str, order_id: str) -> Tuple[int, str]:
        session = getDatabaseSession()
        try:
            order = session.query(NewOrder).filter(
                NewOrder.order_id == order_id).first()
            if not order:
                return error.error_invalid_order_id(order_id)

            if str(order.user_id) != user_id:
                return error.error_authorization_fail()

            code, msg = User().check_password(user_id, password)
            if code != 200:
                return code, msg

            if order.paid:
                return error.error_already_paid(order_id)

            if order.cancelled:
                return error.error_order_cancelled(order_id)

            curTime = datetime.now()
            timeInterval = curTime - order.order_time
            if timeInterval.seconds >= self.paytimeLimit:
                order.cancelled = True
                session.commit()
                return error.error_order_cancelled(order_id)

            buyer = session.query(User).filter(User.user_id == user_id).first()
            store = session.query(UserStore).filter(
                UserStore.store_id == order.store_id).first()
            seller = session.query(User).filter(
                User.user_id == store.user_id).first()

            if not buyer or not store:
                return error.error_non_exist_user_id(user_id)
            balance = getBalance(user_id)

            if balance < order.total_price:
                return error.error_not_sufficient_funds(order_id)

            buyer.balance -= order.total_price
            seller.balance += order.total_price
            order.paid = True

            session.commit()

        except Exception as e:
            print(str(e))
            session.close()
            return 528, str(e)

        finally:
            session.close()

        return 200, "ok"

    def add_funds(self, user_id, password, add_value) -> Tuple[int, str]:
        session = getDatabaseSession()
        try:
            code, msg = User().check_password(user_id, password)
            if code != 200:
                return code, msg
            user = session.query(User).filter(User.user_id == user_id).first()
            if not user:
                return error.error_non_exist_user_id(user_id)
            user.balance += add_value
            session.commit()
        except Exception as e:
            print(str(e))
            session.close()
            return 528, str(e)
        finally:
            session.close()
        return 200, "ok"

    def query_orders(self, user_id, token) -> Tuple[int, str, list]:
        session = getDatabaseSession()
        try:
            code, msg = User().check_token(user_id, token)
            if code != 200:
                return code, msg, ""

            orders = []
            order_list = session.query(NewOrder).filter(
                NewOrder.user_id == user_id).all()

            for order in order_list:
                cur_order = {}
                cur_order_books = []
                order_id = order.order_id
                order_time = order.order_time
                cancelled = order.cancelled

                curTime = datetime.now()
                timeInterval = curTime - order_time
                if timeInterval.seconds >= self.paytimeLimit:
                    order.cancelled = True
                    cancelled = True
                    session.commit()

                for column in order.__table__.columns:
                    cur_order[column.name] = getattr(order, column.name)

                cur_order['cancelled'] = cancelled

                order_details = session.query(NewOrderDetail).filter(
                    NewOrderDetail.order_id == order_id).all()
                for detail in order_details:
                    cur_order_books.append({
                        'book_id': detail.book_id,
                        'count': detail.count,
                        'price': detail.price
                    })

                cur_order['order_books'] = cur_order_books
                orders.append(cur_order)

        except Exception as e:
            print(str(e))
            return 528, str(e), ""

        finally:
            session.close()

        return 200, "ok", orders

    def cancel_order(self, user_id, token, order_id) -> Tuple[int, str]:
        session = getDatabaseSession()
        try:
            code, msg = User().check_token(user_id, token)
            if code != 200:
                return code, msg

            order = session.query(NewOrder).filter(
                NewOrder.order_id == order_id).first()
            if not order:
                return error.error_invalid_order_id(order_id)

            order_time = order.order_time
            curTime = datetime.now()
            timeInterval = curTime - order_time

            if timeInterval.seconds >= self.paytimeLimit:
                order.cancelled = True
                session.commit()
                return error.error_order_cancelled(order_id)

            if order.cancelled:
                return error.error_order_cancelled(order_id)

            if order.paid:
                buyer = session.query(User).filter(
                    User.user_id == order.user_id).first()
                store = session.query(UserStore).filter(
                    UserStore.store_id == order.store_id).first()
                seller = session.query(User).filter(
                    User.user_id == store.user_id).first()

                buyer.balance += order.total_price
                seller.balance -= order.total_price

            order.cancelled = True
            session.commit()
        except Exception as e:
            print(str(e))
            session.close()
            return 528, str(e)

        finally:
            session.close()

        return 200, "ok"
