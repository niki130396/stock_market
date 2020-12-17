from celery import Celery

celery_app = Celery(
    'schedulers',
    backend='redis://localhost',
    broker='redis://localhost',
    include=['financials_spider.yahoo_spider']
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Sofia',
    enable_utc=True
)

if __name__ == '__main__':
    celery_app.start()
