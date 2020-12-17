from celery import Celery

celery_app = Celery(
    'schedulers',
    backend='redis://localhost',
    broker='redis://localhost',
    include=['financials_spider.yahoo_spider']
)


if __name__ == '__main__':
    celery_app.start()
