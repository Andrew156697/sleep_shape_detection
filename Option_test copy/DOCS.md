# 🛌 Home Assistant Add-on: Sleeping Position

This Home Assistant add-on helps monitor and analyze sleeping positions using Mediapipe's 33 landmarks. By detecting posture, the add-on provides actionable insights and suggestions to improve sleep quality.

## Installation

Follow these steps to install the add-on on your Home Assistant system:

1. Navigate to your Home Assistant frontend and go to:
   - **Settings** -> **Add-ons** -> **Add-on Store**.
2. Search for the **"Sleeping Position"** add-on and click on it.
3. Click the **"INSTALL"** button.

## Configuration

This add-on requires six parameters for configuration:

1. **Camera Index (`camera_index`)**: Specify the camera index (integer from 0 to 10). This corresponds to the connected USB or built-in camera.
   
2. **Authentication Parameters**: For data storage and visualization, you'll need the following details:
   - **`my_token`**: Your InfluxDB authentication token.
   - **`my_bucket`**: The name of the bucket in InfluxDB.
   - **`my_org`**: Your organization name in InfluxDB.
   - **`my_url`**: The InfluxDB instance URL (e.g., `https://us-east-1-1.aws.cloud2.influxdata.com/192.168.xxx.xxx`).
   - **`my_duration (senconds)`**: Sampling interval in seconds for collecting data points (minimum = 60).

To obtain these details:
- Register an account on [InfluxDB Cloud](https://us-east-1-1.aws.cloud2.influxdata.com/orgs/59f6f678313bf9b1/load-data/tokens).
- Follow the instructions to create a token, bucket, and other necessary settings.

## Usage

Once configured, the add-on will:
1. Process video input from the specified camera to identify sleeping positions.
2. Log sleeping posture data into InfluxDB for analysis.
3. Provide actionable insights in Home Assistant's frontend.


## Support

For issues or feature requests, please create an issue in the [repository](https://github.com/nott-smartbed/sleep_shape_detection.git).

Enjoy better sleep with actionable insights! 💤
