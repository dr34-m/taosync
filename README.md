<p align="center">
  <strong>English</strong> | <a href="./README_ZH.md">简体中文</a>
</p>

<div align="center">
  <a href="https://github.com/dr34m-cn/taosync">
    <img height="64" alt="TaoSync" src="./taosync-logo.svg"/>
  </a>
  <p><em>TaoSync is an automated synchronization tool with a built-in storage engine and OpenList/AList v3+ compatibility.</em></p>
  <div>
    <a href="https://github.com/dr34m-cn/taosync/blob/main/LICENSE">
      <img src="https://img.shields.io/github/license/dr34m-cn/taosync" alt="License" />
    </a>
    <a href="https://github.com/dr34m-cn/taosync/actions/workflows/build.yml">
      <img src="https://img.shields.io/github/actions/workflow/status/dr34m-cn/taosync/build.yml?branch=main" alt="Build status" />
    </a>
    <a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/backend-python-326c9c.svg" alt="Python" />
    </a>
    <a href="https://vuejs.org/">
      <img src="https://img.shields.io/badge/frontend-vue-42b883.svg" alt="Vue" />
    </a>
    <a href="https://github.com/dr34m-cn/taosync/releases">
      <img src="https://img.shields.io/github/release/dr34m-cn/taosync" alt="Latest version" />
    </a>
    <a href="https://github.com/dr34m-cn/taosync/releases">
      <img src="https://img.shields.io/github/downloads/dr34m-cn/taosync/total?color=%239F7AEA&logo=github" alt="Downloads" />
    </a>
    <a href="https://hub.docker.com/r/dr34m/tao-sync">
      <img src="https://img.shields.io/docker/pulls/dr34m/tao-sync?color=%2348BB78&logo=docker&label=pulls" alt="Docker Hub pulls" />
    </a>
  </div>
</div>

---

Taotao is my daughter's nickname.

I originally created this project to preserve photos of Taotao as she grows up, hence the name `TaoSync`.

**If you find TaoSync useful, please star the repository. Thank you!** [GitHub](https://github.com/dr34m-cn/taosync) [Gitee](https://gitee.com/dr34m/taosync) [Docker Hub](https://hub.docker.com/r/dr34m/tao-sync)

<details>

<summary>Click to view screenshots</summary>

TaoSync is updated frequently, so these screenshots are for reference only. Refer to the current interface for the latest design.

#### Job Details

![Job details](./README/作业详情.jpg)

#### Engine Management

![Engine list](./README/引擎列表.png)

#### Edit Engine

![Edit engine](./README/引擎编辑.png)

#### Create Job

![Create job](./README/新建作业.jpg)

#### Job List

![Job list](./README/作业列表.png)

#### Task Details

![Task details](./README/任务详情.png)

#### Notification Settings

![Notification settings](./README/通知配置.jpg)

</details>

## Before You Begin

> [!IMPORTANT]
> TaoSync includes a built-in, non-removable `TaoSync` engine, so OpenList is no longer required. You can still add an external OpenList/AList instance when you need its additional drivers.

> [!WARNING]
> **Do not expose TaoSync directly to the public internet. You do so at your own risk!**
>
> TaoSync includes some security measures, but absolute security cannot be guaranteed. If external access is necessary, use a strong password and enable `SSL`.

## Use Cases

#### 1. Synchronized Backups

Back up local files to multiple cloud drives, FTP servers, or similar storage services, or synchronize files between multiple cloud drives.

TaoSync can scan specified directories for differences on a schedule. Full sync mode makes the destination match the source, while Add only mode copies only files that exist in the source but not in the destination.

#### 2. Scheduled Downloads

You can create a one-time job by specifying the year, month, day, hour, minute, and second using `cron`. This lets TaoSync automatically download files from a specific cloud drive to local storage during off-peak hours.

## Features

* Free and open source, open to public review, and available on virtually all common platforms
  * windows-amd64
  * windows-arm64
  * darwin-amd64
  * darwin-arm64
  * linux-amd64
  * linux-arm64
  * linux-386
  * linux-arm-v6
  * linux-arm-v7
  * linux-s390x
  * linux-ppc64le
  * Android
* Executables are automatically built and released through [GitHub Actions](https://docs.github.com/en/actions), making the entire build process public and transparent and minimizing the risk of tampered builds
* Ready-to-use Docker image
* Responsive interface for both desktop and mobile devices
* Clean removal: simply delete TaoSync when you no longer need it; it leaves no residual files or dependencies and does not affect other applications
* Login passwords are stored in the database using a one-way hash, and password resets are supported. If you set the initial password through a configuration file or environment variable, protect that configuration carefully
* Runs offline except for storage services configured by the user and never uploads user data to the TaoSync project
* Comprehensive error handling for stable, reliable, and internally consistent operation. Errors may happen, but crashes never do (or so I think)
* Detailed logging: all errors are recorded
* A built-in, non-removable `TaoSync` engine with local directory, SMB, FTP/FTPS, SFTP (SSH), and Aliyun Drive Open Platform support
* External `OpenList/AList` engines remain fully supported and manageable
* Job management: create, delete, enable, disable, edit, and manually run jobs
* Exclusion rules for preventing specified directories or files from being synchronized
* File-size filtering with independently configurable minimum and maximum values
* Three synchronization modes: Add only, Full sync, and Move mode
* Source Directory Mode for all three modes, allowing subsequent jobs to scan only the source and compare it with a database snapshot
* Scheduled synchronization by interval, `cron`, or manual invocation
* Real-time visualization of per-file progress, overall progress, synchronization speed, the file currently being synchronized, estimated completion time, and more
* Controllable storage usage: configure retention periods for task records and logs to keep TaoSync's storage footprint within a predictable range
* Notifications through DingTalk group bots or ServerChan after a task succeeds or fails

## Usage

### Built-in TaoSync Engine

The `TaoSync` engine is created automatically on first startup and initially has no directories. Open its directory manager and add a virtual directory backed by one of these storage types:

* Local directory: browse and select an existing absolute path visible to the TaoSync process. For Docker, mount the host directory into the container first.
* SMB: an SMB 2/3 server and share, credentials, and an optional root within the share. The host field can scan the `/24` networks of TaoSync's active private IPv4 addresses for devices accepting TCP 445; manual entry remains available.
* FTP: FTP or explicit TLS (AUTH TLS), credentials, and an optional remote root. The server must support `MLSD`, which TaoSync uses to distinguish files, directories, and unsafe link-like entries without leaving the configured root.
* SFTP (SSH): a server, port, username, and remote root, authenticated by either a password or pasted PEM/OpenSSH private key with an optional passphrase. The `SHA256:` server host-key fingerprint is optional; use connection testing to obtain it, then save it to lock future connections to that key. Uploads use a temporary file and atomic rename; overwriting existing files requires the server's OpenSSH POSIX rename extension.
* Aliyun Drive: create an application in the [Aliyun Drive Developer Portal](https://www.aliyundrive.com/developer), then obtain `client_id`, `client_secret`, and `refresh_token` through official OAuth. TaoSync uses the official OpenFile API at `openapi.alipan.com` and persists rotated refresh tokens automatically.

After selecting `TaoSync` in a job, paths appear as `/<virtual-directory-name>/...`. File-size comparison, copying, directory creation, deletion, and progress tracking run inside TaoSync. Copies between different storage backends stream through the TaoSync process.

SFTP v3 cannot provide a portable no-follow guarantee across every server-side path race. Use an SSH account restricted by server-side `chroot`, or make the configured remote root writable only by that account. Storage credentials, including SFTP passwords and private keys, currently follow the existing engine behavior and are stored in TaoSync's SQLite database without at-rest encryption; protect the `data` directory accordingly.

### Source Directory Mode

Every successfully completed job stores a complete source-directory snapshot in the database. Add only, Full sync, and Move mode can all enable Source Directory Mode. A first run without a usable snapshot still scans both source and destination; subsequent runs scan only the source and generate operations by comparing relative paths, entry types, file sizes, and a backend version fingerprint when one is available.

The snapshot is replaced atomically only after a complete source scan and a fully successful job. An interrupted scan or a failed copy or delete leaves the previous snapshot in place so the next run retries the work. Changing the engine, source or destination paths, synchronization method, exclusion rules, or file-size filters invalidates the snapshot and makes the next run scan the destination again. Move mode copies to every destination before deleting each source file once.

Because Source Directory Mode does not read destinations, it cannot detect content independently added, removed, or modified there. Full sync deletes only files explicitly tracked by the snapshot and retains directory shells, avoiding accidental removal of excluded or destination-only files. Temporarily disable Source Directory Mode and complete one job when destination state must be checked again. Same-size source replacements are detected when the backend exposes usable version metadata, but accuracy depends on that backend's metadata precision; FTP and SFTP servers may expose only weak or coarse modification metadata. Move mode rechecks the source without cache before deletion and requires a stable version fingerprint; if that fingerprint is unavailable or changed, it keeps the source and reports the operation as incomplete. Every mode rejects dangerous configurations where source and destination paths are equal or nested, including aliases between built-in mounts that resolve to the same backend location.

### Start TaoSync

* Standalone executable

Download the executable for your platform from [Releases](https://github.com/dr34m-cn/taosync/releases) and run it directly.

* Docker

```sh
docker run -d --restart=always -p 8023:8023 -v /opt/data:/app/data --name=taoSync dr34m/tao-sync:latest
```

Or use Docker Compose:

```yaml
version: '3.8'

services:
  tao-sync:
    image: dr34m/tao-sync:latest
    container_name: taoSync
    restart: always
    ports:
      - "8023:8023"
    volumes:
      - /opt/data:/app/data
```

Replace `/opt/data` with the directory you want to use. On some NAS devices, such as UGREEN NAS, you can use a relative path, for example `./config:/app/data`.

#### Docker Compose with OpenList

Use the following Compose file to start TaoSync and OpenList together:

```yaml
services:
  openlist:
    image: openlistteam/openlist:latest
    container_name: openlist
    user: "0:0"
    restart: unless-stopped
    ports:
      - "5244:5244"
    environment:
      UMASK: "022"
      TZ: Asia/Shanghai
    volumes:
      - ./openlist-data:/opt/openlist/data

  tao-sync:
    image: dr34m/tao-sync:latest
    container_name: taoSync
    restart: unless-stopped
    depends_on:
      - openlist
    ports:
      - "8023:8023"
    volumes:
      - ./taosync-data:/app/data
```

After startup, open OpenList at `http://127.0.0.1:5244` and TaoSync at `http://127.0.0.1:8023`. When adding the engine in TaoSync, use `http://openlist:5244` as the OpenList URL. The service name works as the hostname inside the Compose network.

Current OpenList images no longer use the `PUID` and `PGID` environment variables. This example uses `user: "0:0"` for broad compatibility; for least-privilege operation, replace it with the host UID/GID that should run OpenList and ensure that user can write to `./openlist-data`. See the [OpenList Docker documentation](https://doc.oplist.org/guide/installation/docker) for details.

### Use TaoSync

Open `http://127.0.0.1:8023`.

The default username is `admin`. If the initial password is configured as `RANDOM`, find the generated password in the logs. If you configured a password manually, use that value to sign in. After signing in, go to Settings and change the password immediately.

> [!NOTE]
> If the password does not appear in the console output, check `data/log/sys_xxx.log` in the same directory. It is usually on the first line.

After signing in, open Engine Management and add directories to the built-in TaoSync engine, or add an external OpenList/AList engine. Then go to Job Management and create a synchronization job.

## Configuration

<details>
<summary>Click to view configuration options</summary>

Configuration precedence: `data/config.ini` > `environment variables` > `default values`. When a higher-priority source is present, all lower-priority sources are **ignored**. Restart TaoSync or its Docker container after changing the configuration.

`expires` controls both the browser login cookie and server-side signed-cookie validation lifetime, in days.

Example `data/config.ini` file (when present, this file has the **highest priority**):

```ini
[tao]
# Initial administrator password; only used when the database is first created.
# RANDOM or an empty value generates a random password.
password=RANDOM
# Listening port
port=8023
# Login session lifetime in days
expires=2
# Log level: 0-DEBUG, 1-INFO, 2-WARNING, 3-ERROR, 4-CRITICAL.
# Higher values produce fewer logs; 1 or 2 is recommended.
log_level=1
# Console log level; available in v0.2.3 and later. Uses the same levels as above.
console_level=2
# System log retention period in days. Older logs are removed automatically; 0 disables automatic cleanup.
log_save=7
# Task record retention period in days. Older records are removed automatically; 0 disables automatic cleanup.
task_save=0
# Task execution timeout in hours. Set this high enough for large backups to complete.
task_timeout=72
```

This file does not exist by default. To use it, create `config.ini` in the `data` directory next to the TaoSync executable and add the content shown above. The file must use `UTF-8` encoding.

| config.ini    | Docker environment variable | Description | Default |
| ------------- | --------------------------- | ----------- | ------- |
| password      | TAO_PASSWORD                | Initial administrator password; only used when the database is first created. `RANDOM` or an empty value generates a random password. The legacy `TAO_PASSWD` variable is also supported | RANDOM |
| port          | TAO_PORT                    | Listening port | 8023 |
| expires       | TAO_EXPIRES                 | Login session lifetime, in days | 2 |
| log_level     | TAO_LOG_LEVEL               | Log level: 0-DEBUG, 1-INFO, 2-WARNING, 3-ERROR, 4-CRITICAL. Higher values produce fewer logs; 1 or 2 is recommended | 1 |
| console_level | TAO_CONSOLE_LEVEL           | Console log level; available in v0.2.3 and later. Uses the same levels as above | 2 |
| log_save      | TAO_LOG_SAVE                | System log retention period, in days. Older logs are removed automatically; 0 disables automatic cleanup | 7 |
| task_save     | TAO_TASK_SAVE               | Task record retention period, in days. Older records are removed automatically; 0 disables automatic cleanup | 0 |
| task_timeout  | TAO_TASK_TIMEOUT            | Task execution timeout, in hours. Set this high enough for large backups to complete | 72 |
| -             | TZ                          | Time zone | Asia/Shanghai |

</details>

## Development Status

The changelog is available [here](https://github.com/dr34m-cn/taosync/tree/main/doc/changelog).

To try a development build, look for the latest tag containing `dev` or `pre` on [Docker Hub](https://hub.docker.com/r/dr34m/tao-sync) or [Releases](https://github.com/dr34m-cn/taosync/releases), such as `v0.1.0-dev-build0`. Development builds may contain obvious errors or serious bugs and are not recommended for beginners.

### Planned (subject to change or cancellation if implementation proves too difficult; no promises)

* Improve the Windows version, including launch at startup, hidden-window operation, start/stop controls, and more [#13](https://github.com/dr34m-cn/taosync/issues/13)
* Support encrypted synchronization through OpenList [#18](https://github.com/dr34m-cn/taosync/issues/18)
* Support encrypted synchronization for the local engine
* Retain the latest N historical versions, with a configurable and potentially unlimited value for N
* Import and export configuration
* One-command scripts to install, update, and uninstall TaoSync on Linux
