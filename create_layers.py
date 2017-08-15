#!/usr/bin/env python

import inkex

class CreateLayersEffect(inkex.Effect):

    def __init__(self):

        inkex.Effect.__init__(self)

        self.OptionParser.add_option('-b', '--basename', action = 'store',
          type = 'string', dest = 'basename', default = 'New Layer {0}',
          help = 'Base name of the new layer')
        self.OptionParser.add_option('-c', '--count', action = 'store',
          type = 'string', dest = 'count', default = '10',
          help = 'Number of layers to create')

    def effect(self):
        basename = self.options.basename
        count = int(self.options.count)

        svg = self.document.getroot()

        for i in range(0, count):
            layer = inkex.etree.SubElement(svg, 'g')
            layer.set(inkex.addNS('label', 'inkscape'), basename.format(i))
            layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')

effect = CreateLayersEffect()
effect.affect()
