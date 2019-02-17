# plotly-dashboard

Dashboard for sensor data using Dash from plot.ly

## Installation & Requirements
- Create a new virtual environment.
- Run `pip install`.
- All commands are run with Python3. Please config or change cmd according to your local environment.

## Usage
- Check MySQL is running, proper database and tables are set.
- Check the configuration for serial port in `serialReceiver.py`.
- Run `python dashboard.py` to start the dashboard webserver. The access url will shown in terminal.
- Run `python serialReceiver.py` to receive and update sensor data.


## `serialReceiver.py`

### Data Format
Each group of data has multiple new lines, each line contains one value
of a sensor data.

Each entry of data in a group is recorded by sensors at the current time.

#### Database
Use MySQL database running on localhost to store and management the data.
> Not using SQLite3 for concurrent access problem

##### Database Data Scheme
**Data from BMS Arduino**:

**temporature**

|id | timestamp | temp1 | ... | temp24 |
|--- |:-:| :-:| :-:| --:|

`id` is auto increment int as primary key,
`timestamp` is the default timestamp when insert.


**voltage**

|id | timestamp | voltage1 | ... | voltage28 |
|--- |:-:| :-:| :-:| --:|

**Data from CAN Arduino**:

**motor**

|id | timestamp | current | rpm | temp |
|--- |:-:| :-:| :-:| --:|

`rpm` round per minutes;
`temp` temprature of motor, null now.

**workCondition**

|id | timestamp | voltage | current | outputVoltage |
|--- |:-:| :-:| :-:| --:|

`voltage` array of voltage, null now.
`current` array of voltage, null now.
`outputVoltage` motor output voltage.


