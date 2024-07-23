## Installing

### Setup your home assistant input number
- In configuration.yaml, type
```yaml
input_number:
  duolingo_streak:
    name: Duolingo Streak
    initial: 0
    min: 0
    max: 99999
    step: 1
    unit_of_measurement: 'days'
input_boolean:
  duolingo_practiced_today:
    name: Duolingo Practiced Today
    initial: off
```
Then reload your config.


## !! I have not tested the following steps on HAOS, opting instead ot use a server running debian.

### Modify the constants

- Copy the contents of `example.env` to `.env`, then edit the newly created file.
- Set your duolingo username
- Set your Home Assistant URL (make sure you don't end it in a `/`)
- Set your Home Assistant long lived token

### Install and set up
- Install the libraries using pip

```
pip3 install -r requirements.txt
```

- Run the api code manually to make sure it's working
```
python3 api.py
```
When running first time, you'll get an error about reading the previous streak value.


### Setting a cron job to run at every 10th minute of the hour
```
crontab -e # Select your preffered editor
```
Type the following, changing your path accordingly:
```
*/10 * * * * /usr/bin/python3 /PATH/TO/api.py
```