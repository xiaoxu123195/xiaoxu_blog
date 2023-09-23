import pymysql

pymysql.version_info = (1, 4, 13, "final", 0)  # 需要指定版本
pymysql.install_as_MySQLdb()
