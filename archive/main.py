

#logger = logging.getLogger()

def init_db_connection():
    db_config = {
        'pool_size': 5,
        'max_overflow': 2,
        'pool_timeout': 3, 
        'pool_recycle': 1800,
    }
    return init_unix_connection_engine(db_config)

def init_unix_connection_engine(db_config):
    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="postgres+pg8000",
            #host=os.environ.get('DB_HOST'),
            #port=os.environ.get('DB_PORT'),
            username=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASS'),
            database=os.environ.get('DB_NAME'),
            query={
                "unix_sock": "/cloudsql/{}/.s.PGSQL.5432".format(
                    os.environ.get('CLOUD_SQL_CONNECTION_NAME')
                )
            }
        ),
        **db_config
    )
    pool.dialect.description_encoding = None
    return pool

db = init_db_connection()




