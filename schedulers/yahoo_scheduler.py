import schedule

from financials_spider.yahoo_spider import run


if __name__ == '__main__':
    schedule.every(5).minutes.do(run)

    while True:
        schedule.run_pending()