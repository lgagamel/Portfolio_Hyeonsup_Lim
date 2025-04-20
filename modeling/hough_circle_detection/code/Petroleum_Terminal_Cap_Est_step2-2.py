import geopandas as gpd
import geovoronoi 
import ogr
import osgeo.osr as osr
import ogr
import math, sys
import numpy as np
import os

class MWVD():
    def CalDist(self,s1,s2): 
        #Aurenhammer's formulae
        d = s1.Distance(s2)        
        return d
    def ApoloniusCircle(self,s1,s2,w1,w2,  extent): #ogrpoint s1,s2, double w1,w2
        global w1_, w2_, mx, my, mx_new, my_new, s1x, s2x, s1y, s2y
        w1_=w1 
        w2_=w2
        #Aurenhammer's formulae
        s1x=s1.GetX()
        s1y=s1.GetY()
        s2x=s2.GetX()
        s2y=s2.GetY()
#        tmp_ratio = max(w1,w2)/min(w1,w2)
#        if tmp_ratio >=1.1: #regular voronoi
        if (w1==w2): #regular voronoi            
            mx=(s1x+s2x)/2.
            my=(s1y+s2y)/2.
            dx=s1x-s2x
            dy=s1y-s2y
            d=extent.GetBoundary().Length()
            curve=ogr.Geometry(ogr.wkbLineString)
            
            if (dy!=0):
                m=math.atan(-1.*(dx/dy))
                curve.AddPoint_2D(-d*math.cos(m)+mx,-d*math.sin(m)+my)
                curve.AddPoint_2D(d*math.cos(m)+mx,d*math.sin(m)+my)
            else:
                curve.AddPoint_2D(mx,-d+my)
                curve.AddPoint_2D(mx,d+my)
            b=extent.GetBoundary()
            shortCurve=curve.Intersection(extent)
            diff=b.Difference(curve)
            boundary=diff.GetGeometryRef(1)
            endPoint=boundary.GetPoint(0)
            boundary.AddPoint_2D(endPoint[0],  endPoint[1])
            ring=ogr.Geometry(ogr.wkbLinearRing)
            for point in boundary.GetPoints():
                ring.AddPoint_2D(point[0],  point[1])
            ring.AddGeometry(boundary)
            domBoundary=ogr.Geometry(ogr.wkbPolygon)
            domBoundary.AddGeometry(ring)
            
        else: #weighted voronoi
            mx=(s1x+s2x)/2.
            my=(s1y+s2y)/2.
            dx=s1x-s2x
            dy=s1y-s2y
            
            # adjust mx my
            mx_new = s1x - dx*w1/(w1+w2)
            my_new = s1y - dy*w1/(w1+w2)            
            
#            print(mx,mx_new,my,my_new,w1,w2)
            mx=mx_new
            my=my_new

            d=extent.GetBoundary().Length()
            curve=ogr.Geometry(ogr.wkbLineString)
            
            if (dy!=0):
                m=math.atan(-1.*(dx/dy))
                curve.AddPoint_2D(-d*math.cos(m)+mx,-d*math.sin(m)+my)
                curve.AddPoint_2D(d*math.cos(m)+mx,d*math.sin(m)+my)
            else:
                curve.AddPoint_2D(mx,-d+my)
                curve.AddPoint_2D(mx,d+my)
            b=extent.GetBoundary()
            shortCurve=curve.Intersection(extent)
            diff=b.Difference(curve)
            boundary=diff.GetGeometryRef(1)
            endPoint=boundary.GetPoint(0)
            boundary.AddPoint_2D(endPoint[0],  endPoint[1])
            ring=ogr.Geometry(ogr.wkbLinearRing)
            for point in boundary.GetPoints():
                ring.AddPoint_2D(point[0],  point[1])
            ring.AddGeometry(boundary)
            domBoundary=ogr.Geometry(ogr.wkbPolygon)
            domBoundary.AddGeometry(ring)
#
#            
#            
#            
##            print(type(w1),w1,type(w2),w2)
#            den=1./(w1*w1-w2*w2);
#            cx=(w1*w1*s2x-w2*w2*s1x)*den
#            cy=(w1*w1*s2y-w2*w2*s1y)*den
#            #print('Center:', cx, cy)
#            d= math.sqrt(((s1x-s2x)*(s1x-s2x) + (s1y-s2y)*(s1y-s2y)))
#            r=w1*w2*d*den
#            #print("Radius:",r)
#            if (r<0): r=r*-1
#            #creating the circle boundary from 3 points
#            arc= ogr.Geometry(ogr.wkbCircularString) 
#            arc.AddPoint_2D(cx+r,cy)
#            arc.AddPoint_2D(cx-r,cy)
#            arc.AddPoint_2D(cx+r,cy)
#            #creating the circle polygon
#            domBoundary=ogr.Geometry(ogr.wkbCurvePolygon)
#            domBoundary.AddGeometry(arc)
        if s1.Intersects(domBoundary):
#            print('case1',type(w1),w1,type(w2),w2)
            return domBoundary
        else:
#            print('case2',type(w1),w1,type(w2),w2)
            return extent.Difference(domBoundary)
    def getMWVLayer(self,  sites, outDS, layerName, extent):
        global site1, site2
        #srs = osr.SpatialReference()
        #srs.ImportFromEPSG(4326)
        #siteslayer=siteDS.GetLayerByName(site_layerName)
        outLayer = outDS.CreateLayer(layerName, geom_type=ogr.wkbPolygon )
        for site1 in sites:
            dominance=extent
#            dist = []
#            for site2 in sites:
#                tmp_d = site1['p'].Distance(site2['p'])
#                dist = dist + [tmp_d]
#            dist_thr = np.sort(dist)[100]
            for site2 in sites:
#                tmp_d = site1['p'].Distance(site2['p'])
#                if (site1!=site2) and (tmp_d<=dist_thr):
                if site1!=site2:
                    twoSitesDominance=self.ApoloniusCircle(site1['p'], site2['p'], site1['w'], site2['w'], extent)
                    dominance=dominance.Intersection(twoSitesDominance)
#                    try:
#                        #print(site1['p'], site2['p'], site1['w'], site2['w'])
#                        twoSitesDominance=self.ApoloniusCircle(site1['p'], site2['p'], site1['w'], site2['w'], extent)
#                        dominance=dominance.Intersection(twoSitesDominance)
#                    except:
#                        pass
            try:
                # Get the output Layer's Feature Definition
                featureDefn = outLayer.GetLayerDefn()
                #featureDefn = siteslayer.GetLayerDefn()
                #print(featureDefn)
                # create a new feature
                outFeature = ogr.Feature(featureDefn)
                #print(outFeature)
                # Set new geometry
                outFeature.SetGeometry(dominance.GetLinearGeometry())
                #print(dominance.GetLinearGeometry())
                # Add new feature to output Layer
                outLayer.CreateFeature(outFeature)
            except:
                pass
        #print(3)
        #outDS.Destroy()
            
    def readSitesFromLayer(self, ds, layerName, weightAttribute):
        layer=ds.GetLayerByName(layerName)
        sites=[]
        for feature in layer:
            w=feature.GetFieldAsDouble(weightAttribute)
            p=feature.GetGeometryRef()
            sites.append({'p':p.Clone(),  'w':w})
        return sites
            
    def getLayerExtent(self, ds,  layerName):
        layer=ds.GetLayerByName(layerName)
        extent=ogr.Geometry( ogr.wkbPolygon)
        lring=ogr.Geometry( ogr.wkbLinearRing)
        le=layer.GetExtent()
        lring.AddPoint(le[0], le[0])
        lring.AddPoint(le[0], le[3])
        lring.AddPoint(le[1], le[3])
        lring.AddPoint(le[1], le[0])
        lring.AddPoint(le[0], le[0])
        extent.AddGeometry(lring)
        d=abs(le[0]-le[2])
        extent=extent.Buffer(d/10., 0)
        return extent

os.chdir(r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P2_Voronoi\beta3')

prj_file  = 'p2_capacity_final2_selected2.prj'
prj = [l.strip() for l in open(prj_file,'r')][0]

input_gpd = gpd.read_file('p2_capacity_final2_selected2.shp')
input_gpd = input_gpd.iloc[[0]]
n=100
for beta in np.array(range(11,22))/n:
    print(beta)
    tmp_beta = str(int(beta*n))
    #for beta in np.array(range(0,21))/10:
    site_ds = 'p2_capacity_final2'
    siteDS=ogr.Open(site_ds+'.shp')
    
    extent_ds = 'p2_capacity_final2'
    extentDS=ogr.Open(extent_ds+'.shp')
    
    out_ds = 'p2_capacity_final2'
    outDS=ogr.Open(out_ds+'.shp',1)

    tmp_output_fp = 'voronoi2_final_b' + tmp_beta
    input_gpd.to_file(tmp_output_fp+'.shp',driver='ESRI Shapefile',crs_wkt=prj)
    tmp_weight_col = 'est_b_' + tmp_beta
    
    runObj=MWVD()    
    sites=runObj.readSitesFromLayer(siteDS, site_ds, tmp_weight_col)
    
    extent=runObj.getLayerExtent(extentDS,  extent_ds)
    runObj.getMWVLayer(sites, outDS, tmp_output_fp, extent)
    