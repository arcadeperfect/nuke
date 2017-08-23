import os

def find_latest():
    node = nuke.selectedNode()
    file = node['file'].getValue()
    path = '/'.join(file.split('/')[0:10])
    versions = os.listdir(path)
    versions.sort()
    path += '/%s' % versions[-1]
    scriptVersion = os.path.basename(file).split('_')[-1].split('.')[0]
    newFile = file.replace(scriptVersion, versions[-1])
    
    print newFile
    
    first = node.frameRange().first()
    last = node.frameRange().last()
    r = nuke.nodes.Read()
    r.setXYpos(int(node['xpos'].getValue()), int(node['ypos'].getValue()+100))
    
    r['file'].fromUserText('%s %s-%s' %(newFile, first, last))

