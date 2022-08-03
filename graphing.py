from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from sqlmodel import select

from models import Temperature

tzinfo = ZoneInfo("Australia/Melbourne")

def get_n_days(n_days,session):
    since_when: float = datetime.timestamp(datetime.now(tzinfo=tzinfo) - timedelta(days=n_days))
    query = select(Temperature)
    query = query.where(Temperature.timestamp > since_when)
    results = session.exec(query.all())
    points = list(sorted(results, key=lambda p: p['timestamp']))
    devices = set(p.device_id for p in points)
    return {d: [{
                    'd': datetime.fromtimestamp(p.timestamp), 
                    't': p.temperature
                   }
                   for p in points if p.device_id == d]
               for d in devices}

def graph_n_days(n_days,session):
    dataset: dict[str, list] = get_n_days(n_days,session)

    # set up plot, axes
    fig = plt.figure(figsize=(9,5))
    ax = fig.add_subplot(111)
    
    # plot data
    format_iter = iter(['b-','r-','g-','b--','r--','g--'])
    for d in dataset:
        ax.plot(
            'd',
            't',
            fmt = next(format_iter),
            data = d
        )

    # format figure
    ax.set_xlabel('date-time')    
    ax.set_ylabel('temperature')    
    ax.tick_params(axis='x', labelrotation=40)    
    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    # save to memory
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0) # goes back to start of file
    return buffer