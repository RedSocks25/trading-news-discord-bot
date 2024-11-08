import requests
from bs4 import BeautifulSoup
from datetime import date

from typing import TypedDict


class EconomicEvent(TypedDict):
  time: str
  currency: str
  impact: str
  event: str



def fetch_economic_events() -> list[EconomicEvent]:
  url = "https://www.investing.com/economic-calendar/"  # Investing.com calendar URL
  response = requests.get(url)
  
  if response.status_code != 200:
    print(f'Failed to fetch data: {response.status_code}')
    return []

  soup = BeautifulSoup(response.text, 'html.parser')

  # Get the table containing the economic events
  table = soup.find('table', {'id': 'economicCalendarData'})

  # Get table rows (tr) from the table that contains the class "js-event-item"
  rows = table.find_all('tr', {'class': 'js-event-item'})

  # List to store the events
  events: list[EconomicEvent] = []

  for row in rows:

    # Skip the row if the impact is "Low Volatility Expected"
    impact = row.find('td', {'class': 'sentiment'}).get('title').strip()
    if impact == 'Low Volatility Expected':
      continue

    economic_event: EconomicEvent = {
      'time':     row.find('td', {'class': 'time'}).text.strip(),
      'currency': row.find('td', {'class': 'flagCur'}).find('span').text.strip(),
      'impact':   impact,
      'event':    row.find('td', {'class': 'event'}).text.strip(),
    }

    events.append(economic_event)
  
  return events


if __name__ == '__main__':
  fetch_economic_events()