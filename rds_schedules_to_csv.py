import pyreadr

for year in range(1999,2022):
    df_schedule = pyreadr.read_r('Schedules/sched_'+str(year)+'.rds')[None]
    df_schedule.to_csv('Schedules/sched_'+str(year)+'.csv')