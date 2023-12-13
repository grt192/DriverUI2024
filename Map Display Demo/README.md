# Map Display Demo
## How this thing work:
### How to display images:
#### Map (AnimeGirl.png in this demo):
Customize a class (getColorLable), which is a subclass of QLable and 
overrides the mousePressEvent method. This method calls the main window's
get() method and passes the click position, pos.
#### Crosshair:
* Since the upper right corner will appear at the position we put in, we
need to put some offset(half of the height/width) to the position.
* Also, we don't want the crosshair to block the map from getting clicked.
Therefore, we set the attribute to TransparentForMouseEvents.
### Mapping from inch to pixels:
#### field23.png
* Width: 3256px
* Height: 1578px
#### Real Field
* Width: 651.25 in
* Height: 315.5 in
#### Apriltags
##### ID 1:
* x: 620.9
* y: 34.4
* z: 180
* w: 3059
* h: 1368
##### ID 2:
* x: 620.9
* y: 100.5
* z: 180
##### ID 3:
* x: 620.9
* y: 166.4
* z: 180
##### ID 4:
* x: 647.1
* y: 258
* z: 180
##### ID 5:
* x: 4.1
* y: 273.5
* z: 0
##### ID 6:
* x: 30.3
* y: 182
* z: 3
##### ID 7:
* x: 30.3
* y: 116
* z: 1.1
##### ID 8:
* x: 30.3
* y: 50
* z: 0
