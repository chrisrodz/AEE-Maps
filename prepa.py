from suds.client import Client
import json

aee_url = 'http://wss.prepa.com/services/BreakdownReport?wsdl'
aee_client = Client(aee_url)


def getAll():
    count = []
    summary = aee_client.service.getBreakdownsSummary()

    for city in summary:
        name = city.r1TownOrCity
        count.append({
            'name': name,
            'incidents': json.loads(getByCity(name))
        })

    return json.dumps(count)


def getByCity(city):
    city = city.upper()
    results = aee_client.service.getBreakdownsByTownOrCity(city)
    total_averias = []

    for result in results:
        total_averias.append({
            'area': result.r2Area,
            'status': result.r3Status,
            'last_update': result.r4LastUpdate
        })

    return json.dumps(total_averias)
