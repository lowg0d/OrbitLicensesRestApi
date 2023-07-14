class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'orbit_licenses'
    MYSQL_TABLE = "licenses"

config = {
    'development': DevelopmentConfig
}