<!-- no toc -->
# Video Manager App

This is a basic Django backend app that does CRUD operations on Videos that are stored on disk.

- [Video Manager App](#video-manager-app)
  - [Deploy the App](#deploy-the-app)
    - [Manual Stuff](#manual-stuff)
    - [Setup](#setup)
    - [Updating the files](#updating-the-files)
      - [Updating Django Code](#updating-django-code)
      - [Updating Nginx Configs](#updating-nginx-configs)
  - [Accessing the APP (APIs)](#accessing-the-app-apis)
    - [Upload Video](#upload-video)
      - [Endpoint](#endpoint)
      - [Parameters](#parameters)
      - [Request](#request)
      - [Response](#response)
    - [Get Video List](#get-video-list)
      - [Endpoint](#endpoint-1)
      - [Request](#request-1)
      - [Response](#response-1)
    - [Get Video Data](#get-video-data)
      - [Endpoint](#endpoint-2)
      - [Parameters](#parameters-1)
      - [Request](#request-2)
      - [Response](#response-2)
    - [Update Video MetaData](#update-video-metadata)
      - [Endpoint](#endpoint-3)
      - [Parameters](#parameters-2)
      - [Request](#request-3)
      - [Response](#response-3)
    - [Delete Video](#delete-video)
      - [Endpoint](#endpoint-4)
      - [Parameters](#parameters-3)
      - [Request](#request-4)
      - [Response](#response-4)
  - [OPS](#ops)
    - [Restarting APP](#restarting-app)
    - [Check app logs](#check-app-logs)
    - [Check Database](#check-database)
    - [Check Nginx](#check-nginx)
  - [Current Limitations and Future Scope](#current-limitations-and-future-scope)
    - [App](#app)
    - [Containerize](#containerize)
    - [Nginx and SSL](#nginx-and-ssl)
    - [CI/CD](#cicd)

## Deploy the App

In this project we use Ansible to deploy the app on a VM. So make sure you have ssh access(with sudo) to VM.

### Manual Stuff

- Updating IP of server in [hosts](ansible/hosts) file.
- Changing `SERVER_DOMAIN` in [constants.py](video_manager/video_manager/constants.py) to server IP or domain. Also if you are on http, you will have to change `playback_url` that you get in response.

### Setup

- Make sure you have ansible setup from where you plan to run the deploy. You will need to generate GitHub token that you can use to clone private repo(<https://github.com/settings/tokens/new>) with `repo` access.
- Updated the **server IP** in hostgroup `django` in inventory `hosts`.
- Create a file called `vpass` which will be your vault password file with value `aaaa` which is your token value. OR run the command to do the same.

  ```bash
  echo "aaaa" > vpass
  ```

- Run the playbook (make sure you are in parent folder of repo, no need to cd to any other dir)

  ```bash
  ansible-playbook -b -K ansible/django_deploy.yml -i ansible/hosts --vault-password-file vpass -u <ssh-username> -e "github_user=<git-username>" -e "github_token=<token>"
  ```

  The ansible flags may change as per how you want to ssh to servers, but should be more or less same.

This will setup everything from database, migrations and app.

### Updating the files

Based on usecase, there are ansible tags defined that you can run.

#### Updating Django Code

To update the code, you need to run the ansible command with the tag `deploy_app`.

#### Updating Nginx Configs

For Nginx conf update run the tag `nginx_deploy`.

## Accessing the APP (APIs)


### Upload Video

<details>

<summary>Make a POST request with the local video file path to upload.</summary>

#### Endpoint

> POST /videos

#### Parameters

`video_file`[REQUIRED]: absolute local file path of video that you want to upload.

`video_name`[REQUIRED]: this will be the name of the video file on server.

`video_folder`[REQUIRED]: name of the folder where the video will be stored. App automatically creates folder if it does not exists. **The value can be empty string or should end with `/`**.

#### Request

```bash
curl --location --request POST '<SRVER IP>/videos/' \
--form 'video_file=@"<VIDEO FILE PATH>"' \
--form 'video_name="<VIDEO NAME>"' \
--form 'video_folder="<DESTINATION VIDEO FOLDER>"'
```

Example:

```bash
curl --location --request POST '35.154.174.194/videos/' \
--form 'video_file=@"/Users/darshit/test.mp4"' \
--form 'video_name="github.mp4"' \
--form 'video_folder="ds/videos/"'
```

#### Response

```json
{
    "id": 3,
    "video_name": "github.mp4",
    "size": "5253880",
    "path": "ds/videos/",
    "duration": "29.568000",
    "codec": "mov,mp4,m4a,3gp,3g2,mj2",
    "container": "isom",
    "playback_url": "https://35.154.174.194/videos/play/ds/videos/github.mp4"
}
```

where,
`size` is size of video in bytes.
`duration` is video duration in seconds.
`playback_url` is URL what you can use to play the video.
</details>

### Get Video List

<details>
<summary>Make a GET request to list down all the videos in DB.</summary>

#### Endpoint

> GET /videos

#### Request

```bash
curl --location --request GET '<SERVER IP>/videos'
```

Example:

```bash
curl --location --request GET '35.154.174.194/videos'
```

#### Response

Response to this GET request is list of videos with all metadata.

```json
{
    "videos": [
        {
            "id": 1,
            "video_name": "testvid.mp4",
            "size": 1,
            "path": "dsdatsme/",
            "duration": 1000.0,
            "codec": "mov,mp4,m4a,3gp,3g2,mj2",
            "container": "isom",
            "playback_url": "https://35.154.174.194/videos/play/dsdatsme/testvid.mp4"
        },
        {
            "id": 2,
            "video_name": "test.mp4",
            "size": 1,
            "path": "dsdatsme2/",
            "duration": 1000.0,
            "codec": "mov,mp4,m4a,3gp,3g2,mj2",
            "container": "isom",
            "playback_url": "https://35.154.174.194/videos/play/dsdatsme2/test.mp4"
        },
        ...
    ]
}
```
</details>

### Get Video Data

<details>
<summary>Make a GET request with video ID to get it's data.</summary>

#### Endpoint

> GET /videos/\<video id>

#### Parameters

`video id`[REQUIRED]: is an integer.

#### Request

```bash
curl --location --request GET '<SERVER IP>/videos/<VIDEO ID>'
```

Example:

```bash
curl --location --request GET '35.154.174.194/videos/3'
```

#### Response

Response will have all video metadata.

```json
{
    "id": 3,
    "video_name": "github.mp4",
    "size": "5253880",
    "path": "ds/videos/",
    "duration": "29.568000",
    "codec": "mov,mp4,m4a,3gp,3g2,mj2",
    "container": "isom",
    "playback_url": "https://35.154.174.194/videos/play/ds/videos/github.mp4"
}
```

</details>

### Update Video MetaData

<details>
<summary>Make a PUT request with following options to update video metadata.</summary>

> **NOTE**: currently only `path` and `name` updates are supported.

#### Endpoint

> PUT /videos/\<video id>

#### Parameters

`video id`[REQUIRED]: is an integer.

`video_name`[OPTIONAL]: send this if you want to rename a file.

`video_folder`[OPTIONAL]: send this if you want to change the path of the file. **The value can be empty string or should end with `/`**.

#### Request

```bash
curl --location --request PUT '<SRVER IP>/videos/<VIDEO ID>' \
--form 'video_name="<NEW VIDEO NAME>"' \
--form 'video_folder="<NEW DESTINATION VIDEO FOLDER>"'
```

Example:

```bash
curl --location --request PUT '35.154.174.194/videos/3' \
--form 'video_name="new_github.mp4"' \
--form 'video_folder="ds/new_videos/"'
```

#### Response

```json
{
    "id": 3,
    "video_name": "new_github.mp4",
    "size": "5253880",
    "path": "ds/new_videos/",
    "duration": "29.568000",
    "codec": "mov,mp4,m4a,3gp,3g2,mj2",
    "container": "isom",
    "playback_url": "https://35.154.174.194/videos/play/ds/new_videos/new_github.mp4"
}
```

The response will have new metadata values along with updated URL.

</details>

### Delete Video

<details>
<summary>Delete a particular video from server.</summary>

#### Endpoint

> DELETE /videos/\<video id>

#### Parameters

`video id`[REQUIRED]: is an integer.

#### Request

```bash
curl --location --request DELETE '<SERVER IP>/videos/<VIDEO ID>'
```

Example:

```bash
curl --location --request DELETE '35.154.174.194/videos/3'
```

#### Response

Response will have all video metadata of the deleted video.

```json
{
    "id": 3,
    "video_name": "github.mp4",
    "size": "5253880",
    "path": "ds/videos/",
    "duration": "29.568000",
    "codec": "mov,mp4,m4a,3gp,3g2,mj2",
    "container": "isom",
    "playback_url": "https://35.154.174.194/videos/play/ds/videos/github.mp4"
}
```

</details>

## OPS

### Restarting APP

SSH to the server and run the following command to restart the app

```bash
service video_app restart
```

To check the status

```bash
service video_app status
```

### Check app logs

```bash
tail -f /tmp/video_app.log
```

### Check Database

```bash
cd /home/<user>/video_app/video_manager
docker-compose ls       # check running
docker-compose restart  # restart DB
```

### Check Nginx

```bash
less /etc/nginx/nginx.conf              # main file
less /etc/nginx/conf.d/video_app.conf   # app conf

service nginx status                    # check nginx process
service nginx restart                   # restart nginx process
nginx -t                                # test config
```

## Current Limitations and Future Scope

### App

- Exception handling can be improved as various failure scenarios are not considered.
- Currently accepts all file format, but the upload will eventyally fail when app runs ffprobe.
- Video conflicts are checked later stage of the app, should be done before
- Use of serializers to sanity request and responses.
- Tests.
- Limit file size properly.

### Containerize

- Move app to docker container so that we dont need to manage virtual env.
- Once thats done, it can be easily deployed to k8s cluster and can be easily managed and scaled.

### Nginx and SSL

- Restrict Nginx to listen only single domain.
- If still plan to use Nginx, add redirect config for HTTP to HTTPS.
- If planning to move to k8s, use ingress and cert-manager. Example files can be found <https://github.com/DSdatsme/golang-api-k8s-ci-cd>.

### CI/CD

- Use github actions to run test cases and build docker images. Example: <https://github.com/DSdatsme/golang-api-k8s-ci-cd>.
