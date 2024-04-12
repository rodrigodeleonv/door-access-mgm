# door-access-mgm

Web interface to configure Door access.

Features:

Admin interface to manage Users, RFID Tags, ...
API to conect with external RDIF Reader service

## Notes with Raspberry Pi and GPIO

Docker Access to Raspberry Pi GPIO Pins
<https://stackoverflow.com/questions/30059784/docker-access-to-raspberry-pi-gpio-pins>


## (Gnome) Keyring

Some problems can occur with poetry and gnome kerying in development machine. In that case, you should disable kerying
<https://github.com/python-poetry/poetry/issues/8623>

```bash
export PYTHON_KEYRING_BACKEND="keyring.backends.fail.Keyring"

# for permanent add this to ~/.bashrc
```
