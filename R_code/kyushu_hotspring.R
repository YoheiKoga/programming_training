## this code is impressed by http://tomoshige-n.hatenablog.com/entry/2014/08/15/002345

library(readxl)
library(ggplot2)
library(deldir)
library(reshape2)
library(plyr)
library(ggmap)
library(scales)

### data read from opendata http://linkdata.org/work/rdf1s451i/kyushu_onsen_kihon_list_api.html
data <- read.delim(f <- file("http://linkdata.org/api/1/rdf1s451i/kyushu_onsen_kihon_list_R.txt", open="r", encoding="UTF-8"), header=T); close(f);

### read only c(name of hotspring(but don't use), latitude, longitude, prefecture)
data2 <- data[,c(2,4,5,8)]

### rename header
names(data2) <- c("name", "latitude", "longitude", "prefecture")

### pick up fukuoka prefecture
data2 <- subset(data2, data2[,4] == "福岡県")


### point map center as median of lat&lon
loc=c(median(data2$longitude), median(data2$latitude))

### get google map data by ggmap
M=ggmap(get_map(location = loc, zoom = 9, source = "google")) + xlab("") + ylab("")

### extract latitude and longitude
dd <- data2[,2:3]


### scatter diagrams with polygons of contour
hull = chull(dd)
hullPointsIndices <- c(hull, hull[1])
hullPoly_df <- data2[hullPointsIndices,]


### plot data so far
# qplot(longitude, latitude, data = dd) +
#   geom_polygon(data = hullPoly_df, colour = 'red', fill = 'red', alpha = I(1/10), size = 1)



### Voronoi division
xrng <- expand_range(range(dd$longitude), .05)
yrng <- expand_range(range(dd$latitude), .05)

dd.deldir <- deldir(x=dd$longitude, y=dd$latitude, rw = c(xrng, yrng))


### plot Delaunay diagram
# qplot(longitude, latitude, data = dd) +
#   geom_segment(aes(x = x1, y = y1, xend = x2, yend = y2), size = .5, data = dd.deldir$delsgs, colour = 'red', alpha = .5)

### triangulate with polygons
trilist <- unclass(triang.list(dd.deldir))
tridf <- melt(trilist, id.vars = c('x', 'y'))[, c(3, 1:2)]
names(tridf) <- c('tri', 'x', 'y')

### plot data so far
# qplot(longitude, latitude, data = dd) +
#   geom_polygon(aes(x=x, y=y, fill=factor(tri)), data = tridf, colour = 'black', alpha = .5) + scale_fill_discrete(guide = FALSE)



### plot data so far on google map
# M +
#   geom_point(aes(x=longitude, y=latitude, colour=factor(prefecture)), size=3, data = data2) +
#   geom_segment(aes(x = x1, y = y1, xend = x2, yend = y2), size = .25, data = dd.deldir$dirsgs, linetype = 2) +
#   theme_bw(base_family = "HiraMaruProN-W4")


### voronoi with polygons
tilelist <- unclass(tile.list(dd.deldir))
tilelist <- lapply(tilelist, function(l) {
  data.frame(x = l$x, y = l$y)
})

tiledf <- melt(tilelist, id.var = c("x", "y"))

names(tiledf) <- c('x', 'y', 'tile')

### voronoi plot on google map
M +
  geom_polygon(aes(x = x, y = y, fill = factor(tile)), data = tiledf, colour = 'black', alpha = .3) +
  geom_point(aes(x = longitude, y = latitude, colour=factor(prefecture)), size=2, data = data2) +
  theme_set(theme_bw(base_size = 12, base_family = "HiraMaruProN-W4"))
