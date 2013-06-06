from suds.client import Client
import json

aee_url = 'http://wss.prepa.com/services/BreakdownReport?wsdl'
aee_client = Client(aee_url)

def getAll():
    count = {}
    summary = aee_client.service.getBreakdownsSummary()
    for city in summary:
        name = city.r1TownOrCity
        results = aee_client.service.getBreakdownsByTownOrCity(name)
        total_averias = []
        for result in results:
            averia = {}
            averia['Area'] = result.r2Area
            averia['Status'] = result.r3Status
            averia['LastUpdate'] = result.r4LastUpdate
            total_averias.append(averia)
        count[name] = total_averias
    return json.dumps(count)