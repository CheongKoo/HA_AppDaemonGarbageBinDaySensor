# HA_AppDaemonGarbageBinDaySensor
Appdaemon program to show a sensor in Hass.IO for garbage bin type in next collection cycle

![Image of Tile](https://github.com/CheongKoo/HA_AppDaemonGarbageBinDaySensor/blob/master/img/GarbageBinTile.png)
![Image of popup](https://github.com/CheongKoo/HA_AppDaemonGarbageBinDaySensor/blob/master/img/Garbage%20Bin%20sensor%20details%20popup.png)

## Notes
* This has been developed as an Appdaemon 3 module. 
* The limitations of my implementaiton is that it assumes that the collection cycle follows a fixed cadence. For my case, the bins are collected on a Monday and repeats every two weeks.
* The code can support as many bins as you like. This is configurable.
* Once the code executes, it will create a new Hass.IO sensor.

## To implement this sensor
1. Install AppDaemon 3.
2. Configure AppDaemon and make sure that you can run the helloworld application.
3. Download this code and put it into the "/config/appdaemon/apps/" folder in your Hass.IO device.
4. In the code make changes for garbage bin types and their cycle. More information given below.
5. In your "/config/appdaemon/apps/apps.yaml" file, put in the following lines of code.
```yaml
GarbageBinDay_sensor:
  module: appd_binDayCalc.py
  class: binCalc
```
## Adding a new bin
Modify the function setupBins(). In the below example, I've added two bin types - a blue bin and a red bin. The second parameter is the date of the collection. Chose a date in the past. And the third parameter is the number of days till the new cycle. In Australia where I live, the cycle is blue bin (recycle) and red bin (organic) alternating every week, hence the two week cycle.
```python
    #-- Setup the bins
    def setupBins(self):
        #-- Initialise the bins
        self.garbageBins.append(binType("BLUE", "13/01/2020", 14))
        self.garbageBins.append(binType("RED", "06/01/2020", 14))
```

## Modify the sensor values
![Image of sensor values](https://github.com/CheongKoo/HA_AppDaemonGarbageBinDaySensor/blob/master/img/Garbage%20Bin%20sensor%20details.png) 
To change the sensor values, modify the contents of the variables below.

``` python
        self.set_state("sensor.next_garbageCollection", state=stateInfo, attributes=\
                       {"binColour": nBinColour, \
                        "nextCollectionDate": nextCollectionDate, \
                        "daysTillNextCollection": daysLeft,
                        "lastUpdated": lastUpdated
                       })
```

Enjoy.
