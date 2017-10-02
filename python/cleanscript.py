### DELETE NODES WITH NO DEPENDENCIES

exclude = ['BackdropNode','Viewer']

for n in nuke.selectedNodes():
    if not n.Class() in exclude:
        if len(n.dependent())==0 and len(n.dependencies())==0:
            nuke.delete(n)


### DELETE DISABLED NODES

exclude = ['BackdropNode','Viewer']

for n in nuke.selectedNodes():
    if not n.Class() in exclude:
        for i in n.knobs():
            if i == 'disable':
            
                if not n['disable'].isAnimated():
                    if n['disable'].getValue() == 1:
                        nuke.delete(n)
            else:
                print 'errrrrr'