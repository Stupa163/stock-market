from rq import Queue
from worker import conn
from utils import look_over_the_market

q = Queue(connection=conn)
q.enqueue(look_over_the_market)
