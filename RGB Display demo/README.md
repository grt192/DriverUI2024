#   RGB Display Demo
## Classes:
### UI Class:
#### Members:
* Main UI elements such as textDisplays and Labels
* An instance of the networktableHelper class
* Instances of signalEmitters
#### Methods:
* This class implements the interface tableDelegate
* rChange: It calls the rSignalEmitter's rSignal's .emit() method to emit signal. 
* gChange: It calls the gSignalEmitter's gSignal's .emit() method to emit signal. 
* bChange: It calls the bSignalEmitter's bSignal's .emit() method to emit signal. 
* updateR: Updates the displayed R value by calling the setText() method
* updateG: Updates the displayed G value by calling the setText() method
* updateB: Updates the displayed B value by calling the setText() method
### SignalEmitter Class
#### Members:
* One pyqtSignal object.
#### Methods:
* No class methods, the pyqtSignal object's methods are called.
### networktableHelper Class:
#### Members:
* networkTable: used to get info from the robot.
* delegate: will be set to the ui class instance.   
The networktableHelper class can call ui class's methods through the delegate.
#### Methods:
* valueChanged: this method is called everytime a value in the table changes.   
It processes the change and call corresponding methods through the delegate.
