import json
from h1_title_parser.models import UserTask, ReportTask

STATE = {"value": "{},{}".format(UserTask.objects.all().count(), ReportTask.objects.all().count())}


# convert objects count to json
def state_event():
    return json.dumps({"type": "state", **STATE})


# Client requested for update, send info if diff
async def check_updates(websocket, path):
    await websocket.send(state_event())
    try:
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            if data["action"] == "check":

                STATE["value"] = "{},{}".format(UserTask.objects.all().count(), ReportTask.objects.all().count())
                await websocket.send(state_event())
            else:
                pass
    except websocket.exceptions:
        pass
