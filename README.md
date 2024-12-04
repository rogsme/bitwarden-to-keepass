# bitwarden-to-keepass
Export (most of) your Bitwarden items into a KeePass database.

<p align="center">
  <img src="https://gitlab.com/uploads/-/system/project/avatar/55488238/logo.png" alt="bitwarden-to-keepass"/>
</p>

## Fork information

This repository is a fork of [davidnemec/bitwarden-to-keepass](https://github.com/davidnemec/bitwarden-to-keepass). 

They did all of the work, I just added the custom URL functionality and created a Docker repository. All props to [davidnemec](https://github.com/davidnemec/)!

## Features

- Exports Bitwarden vault items to KeePass format (.kdbx)
- Supports:
  - Logins with usernames and passwords
  - TOTP seeds and settings
  - Multiple URIs (including iOS and Android app identifiers)
  - Custom fields (text, hidden, boolean)
  - File attachments
  - Secure notes
  - Nested folder structures
- Maintains folder hierarchy from Bitwarden
- Ensures unique entry names by appending item IDs when needed
- Handles custom Bitwarden/Vaultwarden instances

## Usage 

### Environment variables available

- `DATABASE_PASSWORD` (optional): The password you want your KeePass file to have. If not set, the script will ask for a password interactively.
- `DATABASE_NAME` (optional): The name you want your KeePass file to have. If not set, it will default to `bitwarden.kdbx`.
- `BITWARDEN_URL` (optional): A custom Bitwarden/Vaultwarden instance URL. If you are using the official https://bitwarden.com, you can leave this blank.
- `DATABASE_KEYFILE` (optional): Path to a key file for additional KeePass database security.

### Backup location

All backups will be written to `/exports`. You need to mount that volume locally in order to retrieve the backup file.

### Running with Docker

The simplest way to run the tool is using Docker:

```sh
docker run --rm -it -v ./exports:/exports rogsme/bitwarden-to-keepass
```

**Important Docker flags:**
- `--rm`: The container deletes itself after running (prevents credential leakage)
- `-it`: Enables interactive mode (required for credential input)
- `-v ./exports:/exports`: Mounts local directory for the KeePass file output

### Interactive prompts

The tool will prompt for several pieces of information:

1. KeePass database password (if not set via environment variable):
```sh
DATABASE_PASSWORD is not set
Keepass DB password [input is hidden]
```

2. Bitwarden credentials:
```sh
Email address: your@email.com
Master password: [input is hidden]
```

3. Two-factor authentication (if enabled):
```sh
Two-step login code: 123456
```

### Export process

You'll see progress information like this:

```sh
Generating KeePass file /exports/bitwarden.kdbx
2024-02-20 15:12:54 :: INFO :: KeePass database does not exist, creating a new one.
2024-02-20 15:13:20 :: INFO :: Folders done (1).
2024-02-20 15:13:36 :: INFO :: Starting to process 999 items.
2024-02-20 15:13:36 :: INFO :: Saving changes to KeePass database.
2024-02-20 15:13:43 :: INFO :: Export completed.
```

The script automatically locks your vault and logs out:

```sh
Your vault is locked.
You have logged out.
KeePass file /exports/bitwarden.kdbx generated successfully
```

### Retrieving the export

Your KeePass file will be in the mounted exports directory:

```sh
ls exports
bitwarden.kdbx
```

## Known limitations

- Does not support credit card or identity items
- Requires interactive login (no persistent sessions)
- Android and iOS app identifiers are stored as custom properties

## Security considerations

- The tool requires your Bitwarden master password but never stores it
- Each run requires fresh authentication
- The Docker container is removed after each use
- All credentials are handled securely in memory
- The KeePass database is created with your specified password protection

## FAQ

### Why can't I keep my session open?

For security reasons, the Docker container requires fresh authentication each time. This prevents any accidental credential storage and ensures each export starts from a clean state.

### What if I use a self-hosted Vaultwarden instance?

Set the `BITWARDEN_URL` environment variable to your instance URL before running the container:

```sh
docker run --rm -it -v ./exports:/exports -e BITWARDEN_URL="https://your-instance.com" rogsme/bitwarden-to-keepass
```

### Can I use a key file with my KeePass database?

Yes, you can specify a key file path using the `DATABASE_KEYFILE` environment variable. The key file must be accessible to the container.
