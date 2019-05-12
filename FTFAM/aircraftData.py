aircraft = dict()
tank = dict()

aircraft['maximumRange'] = 3600
aircraft['nOfEngines'] = 2
aircraft['OATcutoff'] = 130

aircraft['cruiseMa'] = 0.89
aircraft['cruiseAlt1'] = 31000
aircraft['cruiseAlt2'] = 35000
aircraft['cruiseAlt3'] = 39000
aircraft['NACARecoveryEfficiency'] = 0.35
aircraft['engineOnTimeBeforeTO'] = 90

tank['minimumTankFullTime'] = 610
tank['maximumTankEmptyTime'] = 500

tank['tankPressurized'] = False
tank['pressureDiff'] = 0
tank['pressTimeBeforeTO'] = 0
tank['tempFusTempSurroundingTk'] = 0

tank['engineOff_fullTau'] = 400
tank['engineOff_emptyTau'] = 200
tank['engineOff_deltaT'] = 15

tank['engineOn_fullTau'] = 400
tank['engineOn_emptyTau'] = 200
tank['engineOn_deltaT'] = 15

tank['flight_fullTau'] = 400
tank['flight_emptyTau'] = 200
tank['flight_deltaT'] = 15
