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
```