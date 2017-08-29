import nuke
import nukescripts

def hide_viewer_lines():
    for i in nuke.allNodes('Viewer'):
        i['hide_input'].setValue(True)

nuke.menu('Nuke').addCommand('harding/Hide Viewer Lines', hide_viewer_lines, 'ctrl+shift+h')

#    Harding Backdrop
#
#

def harding_backdrop():
    bc = 1079406079
    b = nukescripts.autoBackdrop()
    b['note_font_size'].setValue(40)
    b['tile_color'].setValue(bc)
    b['label'].setValue(nuke.getInput('Backdrop Label'))

nuke.menu('Nuke').addCommand('harding/Harding Backdrop', harding_backdrop, 'z')


#    Scale Nodes
#
#

def scale_nodes( scaleX, scaleY ):
    nodes = nuke.selectedNodes()    
    amount = len( nodes )    		
    if amount == 0:    return # DO NOTHING IF NO NODES WERE SELECTED

    for n in nodes:
        w=getW(n)/2
        h=getH(n)/2
        x=getX(n)
        y=getY(n)
    
        n.setXYpos(x+(w),y+(h))

    allX = sum( [ n.xpos()+n.screenWidth()/2 for n in nodes ] )  # SUM OF ALL X VALUES
    allY = sum( [ n.ypos()+n.screenHeight()/2 for n in nodes ] ) # SUM OF ALL Y VALUES

    # CENTER OF SELECTED NODES
    centreX = allX / amount
    centreY = allY / amount

    # REASSIGN NODE POSITIONS AS A FACTOR OF THEIR DISTANCE TO THE SELECTION CENTER
    for n in nodes:
        n.setXpos( int ( centreX + ( n.xpos() - centreX ) * scaleX ) )
        n.setYpos( int ( centreY + ( n.ypos() - centreY ) * scaleY ) )

    for n in nodes:
        w=getW(n)/2
        h=getH(n)/2
        x=getX(n)
        y=getY(n)
    
        n.setXYpos(x-(w),y-(h))

def run_scale_nodes():
    if len(nuke.selectedNodes())==0:
        nuke.message('Select some nodes dumby')
    elif len(nuke.selectedNodes())==1:
        nuke.message('You gotta select more than one node dumby')
    else:
        x = nuke.getInput('x scale','2')
        y = nuke.getInput('y scale','2')
        scale_nodes(float(x),float(y))
		
nuke.menu('Nuke').addCommand('harding/Scale Nodes', run_scale_nodes, )


#	Merge shortcuts
#
#

def hardingMask():
    m = nuke.createNode('Merge2')
    m['operation'].setValue('mask')	

def hardingStencil():
    m = nuke.createNode('Merge2')
    m['operation'].setValue('stencil')

def hardingFrom():
    m = nuke.createNode('Merge2')
    m['operation'].setValue('from')

def hardingPlus():
    m = nuke.createNode('Merge2')
    m['operation'].setValue('plus')

def hardingScreen():
    m = nuke.createNode('Merge2')
    m['operation'].setValue('screen')
	
nuke.menu('Nuke').addCommand('harding/Mask', hardingMask, 'ctrl+shift+m' )
nuke.menu('Nuke').addCommand('harding/Stencil', hardingStencil, 'ctrl+shift+s' )
nuke.menu('Nuke').addCommand('harding/From', hardingFrom, 'ctrl+shift+f' )
nuke.menu('Nuke').addCommand('harding/Plus', hardingPlus, 'ctrl+shift+p' )
nuke.menu('Nuke').addCommand('harding/Screen', hardingScreen, )


#	Recursive Load
#
#

import os

debug = True

def switchExt(path,newExt):
    return '.'.join([os.path.splitext(path)[0],newExt])

# scan
# Scans a directory and sub directories and returns a list of image sequnces and a list of still images
def scan(p):
    imageFormats = ["jpeg","jpg","tiff","exr","dpx","png", "mov"]
    sequences = []
    stillImages = []

    if os.path.isdir(p):
        # find file sequences
        if nuke.getFileNameList(p):
            seqs = nuke.getFileNameList(p)
            # filter out directories
            seqs = [os.path.join(p, seq) for seq in seqs if not os.path.isdir(os.path.join(p, seq)) ]
            if seqs:
                # get still images
                stim = [seq for seq in seqs if os.path.splitext(seq)[-1][1:] in imageFormats]
                if stim:
                    stillImages.extend( stim )

                # filter out non sequences
                seqs = [seq for seq in seqs if (" " in seq and os.path.splitext(seq.split(" ")[0])[-1][1:] in imageFormats)]
                if seqs:
                    sequences.extend( seqs )

    for i in os.listdir(p):
        np = p+i+'/'
        if not os.path.isdir(np):
            continue
        newScan = scan(np)
        sequences.extend( newScan[0] )
        stillImages.extend( newScan[1] )
    return sequences, stillImages
            

# recLoad
# runs scan on directory selected through GUI, creates read nodes

def recload():
    path=nuke.getClipname('Choose Folder', multiple=False)
    allSequences = scan(path)  
    allReads = []


    for i in allSequences[0]:
        n=nuke.nodes.Read(file=i.split(" ")[0], first = i.split(" ")[-1].split("-")[0], last= i.split(" ")[-1].split("-")[-1])
        allReads.append(n)
            
    for i in allSequences[1]:
        allReads.append(n)
        n=nuke.nodes.Read(file=i)
        n['file'].fromUserText(i)

nuke.menu('Nuke').addCommand('harding/RecLoad', recload, )


