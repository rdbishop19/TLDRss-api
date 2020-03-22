from apscheduler.schedulers.background import BackgroundScheduler
from rss_updater import rss_updater

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(rss_updater.get_updated_articles, 'interval', minutes=30)
    scheduler.start()