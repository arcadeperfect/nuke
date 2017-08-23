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



