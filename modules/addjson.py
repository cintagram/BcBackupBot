import json

def adddata(settings, srvids):
            THIS_JSON = '''
{"Enrolled": "True"}
'''
            try:
                this_data = json.loads(THIS_JSON)
            except json.JSONDecodeError:
                print("Invalid JSON format.")
            else:
                settings[str(srvids)] = this_data
                return settings
