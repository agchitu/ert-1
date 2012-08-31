#!/usr/bin/env python
#  Copyright (C) 2011  Statoil ASA, Norway. 
#   
#  The file 'kw_test.py' is part of ERT - Ensemble based Reservoir Tool. 
#   
#  ERT is free software: you can redistribute it and/or modify 
#  it under the terms of the GNU General Public License as published by 
#  the Free Software Foundation, either version 3 of the License, or 
#  (at your option) any later version. 
#   
#  ERT is distributed in the hope that it will be useful, but WITHOUT ANY 
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or 
#  FITNESS FOR A PARTICULAR PURPOSE.   
#   
#  See the GNU General Public License at <http://www.gnu.org/licenses/gpl.html> 
#  for more details. 

import os
import unittest
import stat
import math
import ert
import ert.ecl.ecl as ecl
import sys
from   test_util import *

class KWTest( unittest.TestCase ):
    
    def setUp( self ):
        pass

    def fortio_size( self ):
        unrst_file = "data/eclipse/case/ECLIPSE.UNRST"
        file = ecl.EclFile( unrst_file )
        size = 0
        for kw in file:
            size += kw.fortio_size
        
        stat = os.stat( unrst_file)
        self.assertTrue( size == stat.st_size )
        
        
    def test_kw( self , type , data , fmt ):
        name1 = "/tmp/file1.txt"
        name2 = "/tmp/file2.txt"
        kw = ecl.EclKW.new( "TEST" , len(data) , type)
        i = 0
        for d in data:
            kw[i] = d
            i += 1

        file1 = open(name1 , "w")
        kw.fprintf_data( file1 , fmt )
        file1.close()
        
        
        file2 = open(name2 , "w")
        for d in data:
            file2.write( fmt % d )
        file2.close()
        self.assertTrue( file_equal( name1 , name2) )
        os.unlink( name1 )
        os.unlink( name2 )
            

    def fprintf_test( self ):
        self.test_kw( ecl.ECL_INT_TYPE    , [0 , 1 , 2 , 3 , 4 , 5 ]              , "%4d\n")
        self.test_kw( ecl.ECL_FLOAT_TYPE  , [0.0 , 1.1 , 2.2 , 3.3 , 4.4 , 5.5 ]  , "%12.6f\n")
        self.test_kw( ecl.ECL_DOUBLE_TYPE , [0.0 , 1.1 , 2.2 , 3.3 , 4.4 , 5.5 ] , "%12.6f\n")
        self.test_kw( ecl.ECL_BOOL_TYPE   , [True , True , True , False , True]   , "%4d\n")
        self.test_kw( ecl.ECL_CHAR_TYPE   , ["1" , "22" , "4444" , "666666" , "88888888" ] , "%-8s\n")
        




def fast_suite():
    suite = unittest.TestSuite()
    suite.addTest( KWTest( 'fortio_size' ))
    suite.addTest( KWTest( 'fprintf_test' ))
    return suite

                   

if __name__ == "__main__":
    unittest.TextTestRunner().run( fast_suite() )




#def cutoff( x , arg ):
#    if x < arg:
#        return 0
#    else:
#        return x
#
#
#init_file = ecl.EclFile( "data/eclipse/case/ECLIPSE.INIT" )
#permx     = init_file.iget_named_kw("PERMX" , 0 )
#poro      = init_file.iget_named_kw("PORO" , 0 )
#pvt       = init_file.iget_named_kw("PVTNUM" , 0 )
#grid      = ecl.EclGrid( "data/eclipse/case/ECLIPSE.EGRID" )
#
#
#poro3d = grid.create3D( poro   , default = -100)
#
#print "max:%g" % poro.max
#print "min:%g" % poro.min
#
#mask1 = ecl.EclRegion( grid , False )
#mask2 = ecl.EclRegion( grid , False )
#mask1.select_less( poro , 0.15 )
#mask2.select_more( poro , 0.30 ) 
#
#mask3  = mask1.copy()
#mask3 |= mask2
#
#mask1.reset()
#(x,y,z) = grid.get_xyz( ijk = (grid.nx / 2 , grid.ny /2 , grid.nz / 2) )
#mask1.select_above_plane( [0,0,1] , [x,y,z] )
#print mask1.active_list.size
#print mask1.active_list.str( max_lines = None )
#
#print mask2.active_list.size
#print mask3.active_list.size
#
#poro.apply( cutoff , mask = mask1 , arg = 0.05)
#
#
#poro.write_grdecl( open("/tmp/poro_cos.grdecl" , "w") )
#
#poro.add( permx , mask = mask1)
#poro.sub( 1 )
#poro.mul( poro )
#poro.assign( 14.0 )
#poro.div( 7.0 )
#
#new_p = poro / 7.0
#
#poro.write_grdecl( open("/tmp/poro_cos.grdecl" , "w") )
#
#init_file = ecl.EclFile( "data/eclipse/case/ECLIPSE.INIT" )
#permx_kw = init_file.iget_named_kw( "PERMX" , 0 )
#permx_new = ecl.EclKW.new( "PERMX" , 3 , ecl.ECL_FLOAT_TYPE )
#print ecl.ECL_GRID_FILE
#print ecl.ecl_file_enum
#permx_new[0] = 1
#permx_new[1] = 2
#permx_new[2] = 3
#
##init_file.replace_kw( permx_kw , permx_new )
#fortio = ecl.FortIO.writer( "/tmp/init" )
#print fortio
#init_file.fwrite( fortio )
#fortio.close()
#
#poro   = ecl.EclKW.read_grdecl( open( "data/eclipse/case/include/example_poro.GRDECL" , "r") , "PORO" )
#eqlnum = ecl.EclKW.read_grdecl( open( "data/eclipse/case/include/example_eqlnum.GRDECL" , "r") , "EQLNUM" )
#dummy  = ecl.EclKW.read_grdecl( open( "data/eclipse/case/include/example_eqlnum.GRDECL" , "r") , "BJARNE" , ecl_type = ecl.ECL_INT_TYPE)
#
#if dummy:
#    print "Loading BJARNE OK"
#else:
#    print "Loading BJARNE Failed (correctly)"
#
#print "Poro[100] :%g  eqlnum[100]:%d" % (poro[100] , eqlnum[100]) 
#
#if not eqlnum.type == ecl.ECL_INT_TYPE:
#    sys.exit("Type error when loading eqlnum")
#
#p2 = poro[100:160]
#if p2:
#    print p2.header
#print poro
#print pvt.str( max_lines = 8 )
#print eqlnum
#
#print ecl.EclKW.int_kw
#poro.add_int_kw("BJARNE")
#print eqlnum.int_kw
