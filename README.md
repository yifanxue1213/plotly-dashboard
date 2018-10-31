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
