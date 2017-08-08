import nuke
import nukescripts

def hide_viewer_lines():
    for i in nuke.allNodes('Viewer'):
        i['hide_input'].setValue(True)

nuke.menu('Nuke').addCommand('harding/Hide Viewer Lines', hide_viewer_lines, 'ctrl+shift+h')

def harding_backdrop():
    bc = 1079406079
    b = nukescripts.autoBackdrop()
    b['note_font_size'].setValue(40)
    b['tile_color'].setValue(bc)
    b['label'].setValue(nuke.getInput('Backdrop Label'))

nuke.menu('Nuke').addCommand('harding/Harding Backdrop', harding_backdrop, 'z')