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
```
Then reload your config.


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
If you see anything other than a success message, feel free to troubleshoot or open an issue.


### Setting a cron job to run at every 10th minute of the hour
```
crontab -e # Select your preffered editor
```
Type the following, changing your path accordingly:
```
*/10 * * * * /usr/bin/python3 /PATH/TO/api.py
```

- That's it, you should have an entity called `input_number.duolingo_streak` that will update every 10 minutes.