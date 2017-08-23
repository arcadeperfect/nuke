for i in nuke.allNodes("Submitter"):
    i['priority'].setValue(2)

for i in nuke.allNodes("Submitter"):
    i['execute_farm'].execute()


for i in nuke.selectedNodes():
    i['hide_input'].setValue(1)


for i in nuke.selectedNodes():
    i['matchAOVs'].execute()


for i in nuke.selectedNodes("Submitter"):
    print i.name()
    i['sync_with_shotgun'].setValue(0)
    d = nuke.dependencies(i)[0].frameRange()
    i['first_frame'].setValue(d.first())
    i['last_frame'].setValue(d.last())

for i in nuke.allNodes("pgBokeh"):
    i['disable'].setValue(1)

