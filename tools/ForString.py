def isNull(s):
    """
    判断s是否为空，s，s，返回True
    否则返回False
    :param s: 需要验证的字符串
    :return: True，False
    """
    if s and len(str(s).strip()) > 0:
        return False
    else:
        return True


def isNotNull(s):
    """
    判断s长度是否大于1
    大于1返回：True
    否则返回：False
    :param s: 需要验证的字符串
    :return: True，False
    """
    return not isNull(s)


if __name__ == '__main__':
    print(isNull('   '))
