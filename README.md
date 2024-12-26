# Instagram Data Mining Bot

## Overview
This project is designed to perform automated data mining tasks on Instagram, leveraging SQL databases, FTP servers, and external API integrations. The bot fetches and processes data such as hashtags, user information, and posts while emulating mobile app behavior to avoid detection. Additionally, it dynamically identifies and adds new hashtags to the mining queue through an iterative process, enabling extensive and adaptive data collection.

## Features
- Fetch and process Instagram data in batches, allowing for scalable data mining.
- Dynamically add newly discovered hashtags to mining tasks through an iterative process, broadening the dataset.
- Configurable parameters for batch size, sleep times, and iteration limits.
- Integration with MySQL for data storage and queue management.
- Support for FTP server connections to upload media files.
- Error handling and adaptive sleep times to avoid rate limits.
- Automatic login and session management with support for FTP-stored sessions.
- Ability to mine "n" number of posts for each hashtag, including posts related to newly discovered hashtags.

## Iterative Hashtag Mining
One of the key features of this bot is its ability to expand the mining scope dynamically by discovering and adding new hashtags to the mining tasks. During the data collection process, the script analyzes posts for associated hashtags and queues them for subsequent mining. This iterative approach ensures that the bot continuously broadens its dataset, capturing a more comprehensive network of posts and hashtags. The parameter **`-iteration_limit`** interacts closely with the iterator, controlling the depth of mining by limiting the number of iterations. The script can also download "n" number of posts for each hashtag, ensuring thorough coverage of relevant content.

## Prerequisites
To run this project, you will need:

- Python 3.8+
- Required Python libraries (listed in `requirements.txt`)
- MySQL server with appropriate credentials
- Instagram account credentials for API access
- Config files (`config.json` and `session.json`)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/instagram-mining-bot.git
   cd instagram-mining-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your environment:
   - Update `config.json` with MySQL and FTP credentials.
   - Ensure `session.json` contains the required session data for Instagram access, or use login.py

4. (Optional) Set up a proxy:
   - Create a `proxy.txt` file with the proxy address.
   - Uncomment the relevant lines in the script to enable proxy usage.

## Login and Session Management
The script automatically manages Instagram sessions. Before starting mining, it checks for an existing `session.json` locally or on the configured FTP server.

### Login Process:
1. If `session.json` exists locally, it will be used to authenticate.
2. If `session.json` is available on the FTP server, it will be downloaded and used.
3. If no session file is found:
   - The script prompts for Instagram credentials using the command-line arguments `-usr` and `-pass`.
   - A new session is created, saved locally as `session.json`, and uploaded to the FTP server.

Example login parameters:
```bash
python login.py -usr <instagram_username> -pass <instagram_password> -proxy <optional_proxy>
```

## Usage
Run the script with customizable parameters using the command line:

```bash
python queue_sql_web_hashtagTop.py -batch_size <batch_size> -starting <starting_point> -sleep_time <sleep_time> -big_sleep <big_sleep_time> -MUID <muid> -iteration_limit <iteration_limit> -barredora <on/off>
```

### Parameters
- **`-batch_size`**: Number of items to fetch from the SQL queue.
- **`-starting`**: Starting index for the queue.
- **`-sleep_time`**: Time in seconds between Instagram requests.
- **`-big_sleep`**: Time in seconds between SQL fetches.
- **`-MUID`**: Specific MUID to fetch.
- **`-iteration_limit`**: Maximum number of iterations for the fetch function. This parameter interacts closely with the iterator, determining how many cycles the script will perform and controlling the depth of hashtag mining.
- **`-barredora`**: Activate barredora mode (optional).

### Example
```bash
python main.py -batch_size 10 -starting 0 -sleep_time 5 -big_sleep 30 -MUID None -iteration_limit 20 -barredora on
```

## Configuration Files
- **`config.json`**:
  Contains database and FTP server configurations.
  ```json
  {
    "SQL": {
      "username": "your_username",
      "password": "your_password",
      "hostname": "your_hostname",
      "database": "your_database"
    },
    "FTP": {
      "hostname": "ftp_hostname",
      "username": "ftp_username",
      "password": "ftp_password"
    }
  }
  ```

- **`session.json`**:
  Contains session data required for Instagram API access.

## Development
### Main Functions
- **`fetch`**: Core function to process data in batches, handle errors, and manage SQL interactions. This function iteratively adds newly found hashtags to the queue, enabling comprehensive mining.
- **`updateTaskStatus`**: Updates the status of tasks in the SQL database.
- **`idmb_hashtagMediasTop`** and **`idmb_hashtagMediasRecent`**: Fetch top and recent hashtag data from Instagram. These functions allow mining a specified number of posts for each hashtag, including posts linked to hashtags discovered during the mining process.
- **`login`**: Handles login and session file management.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
For questions or feedback, please contact:
- **Name:** Angel R. Abundis
- **Email:** abundiscomunicacion@gmail.com
