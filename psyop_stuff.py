for i in nuke.allNodes("Submitter"):
    i['priority'].setValue(2)

for i in nuke.allNodes("Submitter"):
    i['execute_farm'].execute()