# fb-garbage-collector

<p align="center"><img src="https://mssnt.pl/misc/github/fbgarbagecollector.png"></p>

FB Garbage Collector is a Facebook moderation bot which automatically removes group posts that failed to reach a certain number of reactions within a configured time frame. It operates by taking control of an invisible Chrome window and impersonating a human user. As such, it doesn't need any API permissions from Facebook.

## Features

* Instantly deplorable - no authorization from Facebook required
* Configurable thresholds, time constraints and refresh rates
* Verbose logging with screenshots on error

## Setup

1. Install the required Python packages (see requirements.txt)
2. Install Chrome and ChromeDriver for Selenium
3. Configure the bot via credentials.json and config.json
4. Run `python fbgarbagecollector.py`

Because the bot uses the same interface that a human would, it requires access to a Facebook account with moderator permissions. Creating a separate account is recommended for this purpose. To prevent unauthorized access, consider enabling two-factor authentication.
