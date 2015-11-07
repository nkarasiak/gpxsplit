# Import GPXSplit
import GPXsplit

# First cut : cut gpx file by segment (trkseg)
input("Press Enter to split by segment...")
GPXsplit.cutby.segment()


# Second cut : cut gpx file by track (trk)
input("Press Enter to split by track...")
GPXsplit.cutby.track()


# Third type of cut : by a point
# We need in first Longitude, then Latitude
# GPXsplit.cutby.point(Longitude,Latitude)
input("Press Enter to split by specific point...")
GPXsplit.cutby.point("-86.79069325","34.789063417")
