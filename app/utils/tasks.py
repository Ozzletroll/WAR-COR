from app import scheduler


@scheduler.task("interval", id="1", seconds=3, misfire_grace_time=900)
def job1():

    print("Job 1 executed")
