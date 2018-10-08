# SAM - A Personal Digital Assistant

SAM is a personal digital assistant that can be customized. SAM interfaces with [Dialogflow](https://dialogflow.com/), 
making it easy to create new, custom intents. As long as the input data is formatted properly, any 
Natural Language Processor will work.


## Getting Started

In order to run SAM, follow these steps:

1. Clone this repository using git.

    ```bash
    $ git clone git@github.com:Kubabuba71/SAM.git
    ```
    
    or
    
    ```bash
    $ git clone https://github.com/Kubabuba71/SAM.git
    ```
    
2. Install dependencies using [pipenv](https://github.com/pypa/pipenv)
(for python version control, [pyenv](https://github.com/pyenv/pyenv) is recommended)

    ```bash
    $ pipenv install
    ```
    
    Note that python version 3.6.6 is needed

3. Complete the steps described in [Deployment Prerequisites](https://github.com/Kubabuba71/SAM#deployment-prerequisites)
    
4. To run locally (not deployed on a server)
    ```bash
    $ python local_server.py
    ```
    
5. To run remotely (deployed on a server)
    ```bash
    $ gunicorn sam:app --workers=1
    ```

### Basic Prerequisites

[pipenv](https://github.com/pypa/pipenv) is used for python package dependency management

[pyenv](https://github.com/pyenv/pyenv) is recommended for controlling which python version is used

```
Give examples
```

### Environment Variables

SAM relies on a number of Environment Variables in order for it to function properly. These can be found in 
[sam/constants.py](https://raw.githubusercontent.com/Kubabuba71/SAM/master/sam/constants.py). At the moment, 
all of these are required for sam to work.
(in the future, some can be disabled if desired, for example if the weather functionality is not desired).

| Environment Variable Name | Description | Example |
| ------------- |:-------------:|:-----------:|
| DARK_SKY_KEY | API Key for the Dark Sky API | N/A |
| GOOGLE_MAPS_GEOCODE_KEY | API Key for the Google Maps Geocoding API | N/A |
| GOOGLE_CALENDAR_CLIENT_ID  | Client ID for the Google Calendar API | N/A |
| GOOGLE_CALENDAR_CLIENT_SECRET | Client Secret for the Google Calendar API | N/A |
| GOOGLE_CALENDAR_PROJECT_ID | Client Project ID for the Google Calendar API | N/A |
| GOOGLE_CALENDAR_CUSTOM_CALENDAR_IDS | '_' seperated list of custom Calendars | N/A |
| SPOTIFY_CLIENT_ID | Client ID of the SAM Spotify App | N/A |
| SPOTIFY_CLIENT_SECRET | Client Secret of the SAM Spotify App | N/A |
| SPOTIFY_REDIRECT_URI | Redirect URI of the SAM Spotify App | https://www.samhost.com/spotify_callback' |
| DIALOGFLOW_CLIENT_ACCESS_TOKEN | Client Access Token for Dialogflow | N/A |

## Deployment Prerequisites

Before deployment is possible, a number of preparatory steps must be taken.

In the following, 'https://sam_host.com' is refers to the domain at which SAM is reachable

1. Go to the [Dark Sky](https://darksky.net/dev) website and sign up
    - Remember the Secret Key (used as ```DARK_SKY_KEY``` Environment Variable)
   
2. Inside of Google Cloud Platform, create a new project (sam-server, for example)
    - Remember the Project ID (used as ```GOOGLE_CALENDAR_PROJECT_ID``` Environment Variable)

3. Activate the Geocoding API:
    - Inside of the new Google Cloud Platform project, activate the Geocoding API
    - Create new credentials specifically for the Geocoding API
    - Remember the API Key (used as ```GOOGLE_MAPS_GEOCODE_KEY``` Environment Variable)
    
4. Go to [Google Calendar API Quickstart](https://developers.google.com/calendar/quickstart/python) and click on 
'ENABLE THE GOOGLE CALENDAR API'.
    - Select your sam-server you created in Step 2
    - Remember the Client ID and Client Secret (used as ```GOOGLE_CALENDAR_CLIENT_ID``` and 
    ```GOOGLE_CALENDAR_CLIENT_SECRET``` Environment Variables)
    
5. Spotify App has to be created so that SAM can interface with Spotify
    - Create the [Spotify App](https://developer.spotify.com/dashboard/applications)
    - Set the Redirect URIs to 'https://sam_host.com/spotify_callback'' and 'https://localhost:5000/spotify_callback'
    - Remember the Client ID and Client Secret (used as ```SPOTIFY_CLIENT_ID``` and 
    ```SPOTIFY_CLIENT_SECRET``` Environment Variables)

6. Go to [Dialogflow](https://dialogflow.com/) and sign up for an account
    - Create a new Agent
    - Import intents and entities from _ (file will be provided in the near future)
    - Inside of settings, do the following:
        - Enable 'V2 API' under 'API Version'
        - Remember the Client Access Token (used as ```DIALOGFLOW_CLIENT_ACCESS_TOKEN``` Environment Variable)
    - Inside of Fulfillment, do the following:
        - Set the 'URL' to 'https://sam_host.com/dialogflow_webhook'
7. Run SAM
    - Once the above steps are complete, proceed to the [Running SAM](https://github.com/Kubabuba71/SAM#running-sam) 
    section

## Running SAM

Once [Deployment Prerequisites](https://github.com/Kubabuba71/SAM#deployment-prerequisites) has been completed, 
simply run the following command on the deployment server:

```bash
$ gunicorn sam:app --workers=1
```

Otherwise, deploy to [Heroku](https://www.heroku.com/), which will use the 
[Procfile](https://github.com/Kubabuba71/SAM/blob/master/Procfile) to start the server 
(don't forget to set the environment variables first).

## Versioning

Versioning is based on [Semantic Versioning](http://semver.org/). 
For the versions available, see the [releases on this repository](https://github.com/Kubabuba71/SAM/releases). 
