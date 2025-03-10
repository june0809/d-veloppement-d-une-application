from apscheduler.schedulers.blocking import BlockingScheduler
from model import Table

def job():
    choix = 0  # ou 1, ou 2 en fonction de la table que vous souhaitez mettre à jour
    Table.delete_table_data(choix)  # Supprime les anciennes données
    Table.insert_data(choix)  # Insère les nouvelles données

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'cron', hour=18)  # Planifiez le travail pour qu'il s'exécute tous les jours à minuit
    try:
        print("Scheduler started")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
