# 数据库课程第二次大作业报告

## 测试覆盖率数据

```
-- coverage: platform linux, python 3.11.3-final-0 --
Name                              Stmts   Miss  Cover
-----------------------------------------------------
be/__init__.py                        0      0   100%
be/conf.py                            1      0   100%
be/model/__init__.py                  0      0   100%
be/model/buyer.py                   171     24    86%
be/model/database.py                 24      1    96%
be/model/error.py                    33      3    91%
be/model/search.py                   42      8    81%
be/model/seller.py                   86     16    81%
be/model/tables.py                   96      0   100%
be/model/user.py                    154     26    83%
be/serve.py                          37      6    84%
be/view/__init__.py                   0      0   100%
be/view/auth.py                      42      0   100%
be/view/buyer.py                     50      0   100%
be/view/search.py                    21      0   100%
be/view/seller.py                    37      0   100%
fe/__init__.py                        0      0   100%
fe/access/__init__.py                 0      0   100%
fe/access/auth.py                    32      0   100%
fe/access/book.py                    64      0   100%
fe/access/buyer.py                   49      0   100%
fe/access/new_buyer.py                8      0   100%
fe/access/new_seller.py               8      0   100%
fe/access/search.py                  17      0   100%
fe/access/seller.py                  37      0   100%
fe/bench/__init__.py                  0      0   100%
fe/bench/run.py                      13      0   100%
fe/bench/session.py                  47      0   100%
fe/bench/workload.py                125      1    99%
fe/conf.py                           11      0   100%
fe/conftest.py                       17      4    76%
fe/test/gen_book_data.py             50      1    98%
fe/test/test_add_book.py             36      0   100%
fe/test/test_add_funds.py            30      0   100%
fe/test/test_add_stock_level.py      42      0   100%
fe/test/test_bench.py                 8      2    75%
fe/test/test_book_info.py            25      0   100%
fe/test/test_cancel_order.py         85      2    98%
fe/test/test_create_store.py         20      0   100%
fe/test/test_deliver_order.py        69      1    99%
fe/test/test_fuzzy_search.py         42      0   100%
fe/test/test_login.py                28      0   100%
fe/test/test_new_order.py            40      0   100%
fe/test/test_password.py             33      0   100%
fe/test/test_payment.py              80      1    99%
fe/test/test_query_orders.py         30      0   100%
fe/test/test_register.py             31      0   100%
-----------------------------------------------------
TOTAL                              1871     96    95%
========== 46 passed in 134.04s (0:02:14) ===========
```