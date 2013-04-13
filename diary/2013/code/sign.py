#coding: utf-8

from redis import Redis

r = Redis()


"""
key maker
"""

def _sign_key(date):
    """
    生成签到日期的键，例如 2013-4-13::signed
    """
    return "{0}::signed".format(date)

def _sign_count_key(user):
    """
    生成用户签到计数器的键，例如 tom::sign_count
    """
    return "{0}::sign_count".format(user)


"""
api implement
"""

def sign(user, date):
    """
    用户在指定日期签到
    """
    # 注意，为了保持示例实现的简单性
    # 目前的这个实现不能防止一个用户在同一天多次签到
    # 解决这个问题需要使用事务或者 Lua 脚本
    r.incr(_sign_count_key(user))
    r.sadd(_sign_key(date), user)

def signed(user, date):
    """
    用户在指定日期已经签到了吗？
    """
    return r.sismember(_sign_key(date), user)

def sign_count_of(user):
    """
    返回给定用户的签到次数
    """
    count = r.get(_sign_count_key(user))

    if count is None:
        return 0
    else:
        return int(count)

def top_sign(top_sign_name, *dates):
    """
    将给定日期内的签到排名保存到 top_sign_name 键中，
    并从高到低返回排名结果。
    """
    date_keys = map(_sign_key, dates)
    r.zunionstore(top_sign_name, date_keys)
    return r.zrevrange(top_sign_name, 0, -1, withscores=True)

def full_sign(full_sign_name, *dates):
    """
    将给定日期内的全勤记录保存到 full_sign_name 键中，
    并返回全勤记录。
    """
    date_keys = map(_sign_key, dates)
    r.sinterstore(full_sign_name, date_keys)
    return r.smembers(full_sign_name)


"""
test
"""

if __name__ == "__main__":

    r.flushdb()


    # test sign() and signed()

    assert(
        not signed("tom", "2013-4-13")
    )

    sign("tom", "2013-4-13")

    assert(
        signed("tom", "2013-4-13")
    )

    r.flushdb()


    # test sign_count_of()

    assert(
        sign_count_of("tom") == 0
    )

    sign("tom", "2013-4-13")

    assert(
        sign_count_of("tom") == 1
    )

    sign("tom", "2013-4-14")

    assert(
        sign_count_of("tom") == 2
    )

    r.flushdb()


    # test top_sign() and full_sign()

    days = ["2013-4-13", "2013-4-14", "2013-4-15"]

    sign("tom", days[0])
    sign("peter", days[0])
    sign("john", days[0])

    sign("peter", days[1])
    sign("john", days[1])
    
    sign("peter", days[2])

    ts = top_sign("2013-4-13 to 2013-4-15 top sign", *days)
    assert(
        ts[0] == ("peter", 3.0) and
        ts[1] == ("john", 2.0)  and
        ts[2] == ("tom", 1.0)
    )

    assert(
        full_sign("2013-4-13 to 2013-4-15 full sign", *days) == set(["peter"])
    )

    r.flushdb()
