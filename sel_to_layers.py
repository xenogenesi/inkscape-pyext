#!/usr/bin/env python

import inkex
import sys, copy
from collections import OrderedDict

NSS = {
    u'sodipodi' :u'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
    u'cc'       :u'http://creativecommons.org/ns#',
    u'ccOLD'    :u'http://web.resource.org/cc/',
    u'svg'      :u'http://www.w3.org/2000/svg',
    u'dc'       :u'http://purl.org/dc/elements/1.1/',
    u'rdf'      :u'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    u'inkscape' :u'http://www.inkscape.org/namespaces/inkscape',
    u'xlink'    :u'http://www.w3.org/1999/xlink',
    u'xml'      :u'http://www.w3.org/XML/1998/namespace'
}

class SelToLayersEffect(inkex.Effect):

    # override self.selected and self.getselected to keep user selection order
    
    def __init__(self):

        inkex.Effect.__init__(self)
        self.selected = OrderedDict()
        
        self.OptionParser.add_option('-b', '--basename', action = 'store',
                                     type = 'string',
                                     dest = 'basename',
                                     default = 'layer-{1}-{0}',
                                     help = 'Base name of the new layer')

    def getselected(self):
        """Collect selected nodes"""
        for i in self.options.ids:
            path = '//*[@id="%s"]' % i
            for node in self.document.xpath(path, namespaces=NSS):
                self.selected[str(i)] = node

    def newLayer(self, svg, name='no name'):
        layer = inkex.etree.SubElement(svg, 'g')
        layer.set(inkex.addNS('label', 'inkscape'), name)
        layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
        return layer
        
    def effect(self):
        basename = self.options.basename

        svg = self.document.getroot()
        
        if self.selected:
            i = 0
            for id, node in self.selected.iteritems():
                newNode = copy.deepcopy(node)
                # inkex.debug(newNode.attrib)
                newLayer = self.newLayer(svg, basename.format(newNode.get('id'), i))
                newLayer.append(newNode)
                # optionally delete original selection?
                # node.getparent().remove(node)
                i = i + 1
        else:
            inkex.errormsg("nothing selected")

effect = SelToLayersEffect()
effect.affect()
