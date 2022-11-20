# pyEOCharging

Python Library For interacting with EO Home EV Chargers.

This has only been tested with a EO Mini Pro 2.


Example usage:

```python
import eocharging

conn = eocharging.connection("email_address", "password")

devices = conn.get_devices() #Get list of devices on account
print(devices)

sessions = devices[0].get_sessions()
print(sessions) #Print list of sessions from all time from first device on account

devices[0].disable() #Disable/lock the charger
devices[0].enable() #Enable/unlock the charger

currentChargeOpt = devices[0].get_chargeOpts() #get charger current settings
print(currentChargeOpt.__dict__) #show charger current settings

Note that among other things, get_chargeOpts returns a cpid which is needed to amend options (see set_chargeOpts)

newChargeOpts = eocharging.Device.chargeOpts(cpid=currentChargeOpt.cpid,opMode=newOpMode) #Construct new charger options - for full list, see those returned from get_chargeOpts()
devices[0].set_chargeOpts(newChargeOpts) #Set charger options. cpid is mandatory, plus at least one option to change.
currentChargeOpt = devices[0].get_chargeOpts() #Check new option was applied successfully

```
