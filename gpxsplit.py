# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 18:22:04 2015

@author: lennepkade
"""
# https://www.jmcpdotcom.com/blog/2015/06/01/fixing-up-gpx-ride-data-with-lxml-etree/
#     

# import etree to manage GPX, objectify to remove namespace
from lxml import etree, objectify
# import os for manipulating folder and searching gpx files
import os

print("Get all gpx from script folder and split it into segment to \"result\" folder") 
       
#
class gpxsplit:
    """
    # This class manage gpx in the folder'script.
    ROLE : Open/read gpx,  create result directory to save split gpx
    
    def getfile():
        FUNCTION : List the script directory and get all gpx files
        RETURN : All gpx files in a list 
    def infile.parsefile():
        FUNCTION : Parse gpx file with etree (lxml)
        RETURN : Parsing file, root file, and filename (without extension)
    def folder.resultdir():
        FUNCTION : Create by defaut "result" folder if doesn't exist
        RETURN : Folder name     
    """
    def getfile():
        # Create empty list
        gpxfiles=[]
        # Searching for gpx file in script directory and adding to gpxfiles list
        for file in os.listdir():
            if file.endswith(".gpx"):
                gpxfiles.append(file)
        # Return list with gpx files
        return gpxfiles
    
    def parsefile(infile):
        # File name without extension
        outfileNoExt=infile.replace(".gpx", "")
        # Gpx tree file
        outgpx=etree.parse(infile)
        # Gpx root file
        outroot = outgpx.getroot()
        # Remove Default Namespace
        for elem in outroot.getiterator():
            if not hasattr(elem.tag, 'find'): continue  # (1)
            i = elem.tag.find('}')
            if i >= 0:
                elem.tag = elem.tag[i+1:]
        objectify.deannotate(outroot, cleanup_namespaces=True)
        # Return tree, root, and filename without extension)
        return (outgpx,outroot,outfileNoExt)
    
    def resultdir(folder='result/'):
        # Create result folder if doesn't exist
        if not os.path.isdir(folder):
            os.makedirs(folder)
        return folder
        
    def addmetadata():
        gpx = etree.Element('gpx', xmlns="http://www.topografix.com/GPX/1/1")
        # add metadata to gpx
        gpxmetadata = etree.SubElement(gpx, 'metadata')
        etree.SubElement(gpxmetadata, 'author').text = "GpxSplit"
        etree.SubElement(gpxmetadata, 'link').text = "https://github.com/lennepkade/gpxsplit"

class cutby(gpxsplit):
    """
    # This class split gpx into multiple files
    ROLE : Depending the function, gpx is split depending a special point,
    or into every segment orevery track
    
    def segment():
        FUNCTION : Parse file, manage namespace, and split into different segments
        RETURN : Create a file for each segment with the name "file_seg1.gpx" (1 to X segments)         
    def track():
        FUNCTION : Parse file, manage namespace, and split into different tracks
        RETURN : Create a file for each track with the name "trk1.gpx" (1 to X tracks)
    def point(inLon,inLat):
        FUNCTION : Parse file, manage namespace, and split a file in two depending a point
        If a point doens't exist, will split if a point has a lon and lat higher than given lon/lat.
        RETURN : Create two files with name "file_part1.gpx" and "file_part2.gpx" 
    """
    def segment():
        for file in gpxsplit.getfile():
            gpx,root,noext=gpxsplit.parsefile(file)
            #Get number of segments
            nbseg=int(gpx.xpath("count(//trkseg)"))
            # If more than one segment, splitting file by segment and tell user
            if nbseg>1:
                print(noext,'has',nbseg, 'segments. Splitting file...')
                for id, seg in enumerate(root.iter('trkseg')):
                    # add GPX metadata
                    gpx = etree.Element('gpx', xmlns="http://www.topografix.com/GPX/1/1")
                    # add metadata to gpx
                    gpxmetadata = etree.SubElement(gpx, 'metadata')
                    etree.SubElement(gpxmetadata, 'author').text = "GpxSplit"
                    etree.SubElement(gpxmetadata, 'link').text = "https://github.com/lennepkade/gpxsplit"  
                    etree.SubElement(gpxmetadata, 'name').text = noext+' split by segment'
                    # add TRK tag (children of GPX)
                    trk = etree.SubElement(gpx, "trk")
                    # add all elements in each segment (trkpt, ele, time...)
                    trk.append(seg)   
                    # id begins with 0, add 1 to start at 1
                    id+=1
                    # create a file for each seg
                    # call resultdir() to create result folder if doesn't exist
                    with open(gpxsplit.resultdir()+noext+'_seg'+str(id)+'.gpx', mode='wb') as doc:
                        doc.write(etree.tostring(gpx, pretty_print=True))
            else: # script has nothing to do
                print(noext,'has only one or no segment. No change')
        # Tell the user operation is done and show folder
        print("Done")
        print("Split files has been stored in \""+gpxsplit.resultdir()+"\" folder")
        
    def track():
        for file in gpxsplit.getfile():
            gpx,root,noext=gpxsplit.parsefile(file)
            nbtrk=int(gpx.xpath("count(//trk)"))
            if nbtrk>1:
                print(noext,'has',nbtrk, 'trk. Splitting file...')
                for id, trk in enumerate(root.findall('trk')):
                    # add GPX metadata
                    gpx = etree.Element('gpx', xmlns="http://www.topografix.com/GPX/1/1")
                    # add metadata to gpx
                    gpxmetadata = etree.SubElement(gpx, 'metadata')
                    etree.SubElement(gpxmetadata, 'author').text = "GpxSplit"
                    etree.SubElement(gpxmetadata, 'link').text = "https://github.com/lennepkade/gpxsplit"  
                    etree.SubElement(gpxmetadata, 'name').text = noext+' split by track'
                    # add all seg
                    gpx.append(trk)   
                    # id begins with 0, add 1 to start at 1
                    id+=1
                    # create a file for each track
                    # call resultdir() to create result folder if doesn't exist
                    with open(gpxsplit.resultdir()+noext+'_trk'+str(id)+'.gpx', mode='wb') as doc:
                        doc.write(etree.tostring(gpx, pretty_print=True))
            else: # script has nothing to do
                print(noext,'has only one or no trk. No change')  
        # Tell the user operation is done and show folder
        print("Done")
        print("Split files has been stored in \""+gpxsplit.resultdir()+"\" folder")
                        
    def point(inLon,inLat):
        for file in gpxsplit.getfile():
            gpx,root,noext=gpxsplit.parsefile(file)
            for trk in root.findall('trk'):
                # create a gpx for each part and add metadata
                gpx1 = etree.Element('gpx', xmlns="http://www.topografix.com/GPX/1/1")
                gpxmetadata = etree.SubElement(gpx1, 'metadata')
                etree.SubElement(gpxmetadata, 'author').text = "GpxSplit"
                etree.SubElement(gpxmetadata, 'link').text = "https://github.com/lennepkade/gpxsplit"  
                etree.SubElement(gpxmetadata, 'name').text = noext+' split by specific point'
                gpx2 = etree.Element('gpx', xmlns="http://www.topografix.com/GPX/1/1")
                gpxmetadata = etree.SubElement(gpx2, 'metadata')
                etree.SubElement(gpxmetadata, 'author').text = "GpxSplit"
                etree.SubElement(gpxmetadata, 'link').text = "https://github.com/lennepkade/gpxsplit"  
                etree.SubElement(gpxmetadata, 'name').text = noext+' split by specific point'
                trk1 = etree.SubElement(gpx1, "trk")
                trk2 = etree.SubElement(gpx2, "trk")
                print("Splitting file :",noext)
                for seg in root.iter("trkseg"):
                    # create a segment per gpx file
                    
                    seg1 = etree.SubElement(trk1, "trkseg")
                    seg2 = etree.SubElement(trk2, "trkseg")
                    for track in root.iter("trkpt"):
                        # Add trks to part 1
                        if track.attrib['lat']<=inLat and track.attrib['lon']<=inLon:                           
                            seg1.append(track)
                            with open(gpxsplit.resultdir()+noext+'_part1'+'.gpx', mode='wb') as doc:
                                       doc.write(etree.tostring(gpx1, pretty_print=True))
                        # Add trks to part 2  
                        else:
                            seg2.append(track)
                            with open(gpxsplit.resultdir()+noext+'_part2'+'.gpx', mode='wb') as doc:
                                       doc.write(etree.tostring(gpx2, pretty_print=True))
        # Tell the user operation is done and show folder
        print("Done")
        print("Split file has been stored in \""+gpxsplit.resultdir()+"\" folder")
            
if __name__ == '__main__':
    #cutby.point("-86.79069325","34.789063417")
    cutby.track()
    #cutby.segment()
    
