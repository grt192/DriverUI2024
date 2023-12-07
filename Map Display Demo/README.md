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
Therefore we set the attribute to TransparentForMouseEvents.