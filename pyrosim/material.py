from pyrosim.commonFunctions import Save_Whitespace

class MATERIAL: 

    def __init__(self, color, rgb):

        self.depth  = 3

        self.string1 = '<material name="' + color + '">'

        self.string2 = '    <color rgba="' + str(rgb[0]) + ' ' + str(rgb[1]) + ' ' + str(rgb[2]) + ' 1.0"/>'
        self.string3 = '</material>'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )
