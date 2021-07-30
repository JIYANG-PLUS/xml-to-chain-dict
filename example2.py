from typing import List
import xmltocd
from xmltocd import ChainManager

xml_data = """\
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
   <x></x>
   <Document>
      <Folder>
         <name id="out" name="dsad">One Line Diagram</name>
         <open>0</open>
         <Folder>
            <name id="one">SectionOne</name>
            <open>0</open>
            <Folder>
               <name>Node</name>
               <open>0</open>
               <Placemark>
                  <name>5680420</name>
                  <styleUrl>#Style_0</styleUrl>
                  <description />
                  <MultiGeometry type="MultiGeometry" Type="MultiGeometry">
                     <Polygon>
                        <outerBoundaryIs>
                           <LinearRing>
                              <coordinates>-83.6514766,67.0234192 -83.6515403,67.0233918 -83.6515309,67.0233134 -83.6514609,67.0232885 -83.5778406,67.0246267 -83.5777768,67.0246541 -83.5777861,67.0247325 -83.5778560,67.0247574 -83.6514766,67.0234192</coordinates>
                           </LinearRing>
                        </outerBoundaryIs>
                     </Polygon>
                  </MultiGeometry>
               </Placemark>
               <Placemark>
                  <name>25934531</name>
                  <styleUrl>#Style_0</styleUrl>
                  ML60
                  <description />
                  <MultiGeometry type="MultiGeometry" Type="MultiGeometry">
                     <Polygon>
                        <outerBoundaryIs>
                           <LinearRing>
                              <coordinates>-83.6512679,67.0216805 -83.6513317,67.0216531 -83.6513222,67.0215747 -83.6512522,67.0215498 -83.5967049,67.0225434 -83.5966412,67.0225708 -83.5966505,67.0226492 -83.5967204,67.0226741 -83.6512679,67.0216805</coordinates>
                           </LinearRing>
                        </outerBoundaryIs>
                     </Polygon>
                  </MultiGeometry>
               </Placemark>
            </Folder>
         </Folder>
      </Folder>
   </Document>
</kml>
"""

xmlManager: ChainManager = xmltocd.parse_string(xml_data)

# 方式一
node = xmlManager.find_node_by_attrs(id='out')
del_node = xmlManager.popitem(node)

del_node = xmlManager.pop_node_by_attrs(id='out')
del_nodes = xmlManager.pop_nodes_by_attrs(id='out')
