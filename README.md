# bitwarden-to-keepass
Export (most of) your Bitwarden items into a KeePass database.

<p align="center">
  <img src="https://gitlab.com/uploads/-/system/project/avatar/55488238/logo.png" alt="bitwarden-to-keepass"/>
</p>

## Fork information

This repository is a fork of [davidnemec/bitwarden-to-keepass](https://github.com/davidnemec/bitwarden-to-keepass). 

They did all of the work, I just added the custom URL functionality and created a Docker repository. All props to [davidnemec](https://github.com/davidnemec/)!

## How does it works?
It uses the official [bitwarden-cli](https://bitwarden.com/help/article/cli/) client to export your items from the Bitwarden vault and move them into your KeePass database - that includes logins (with TOTP seeds, URIs, custom fields, attachments, notes) and secure notes.

## Usage 

### Environment variables available

- `DATABASE_PASSWORD` (optional): The password you want your KeePass file to have. If not set, the script will ask for a password interactively.
- `DATABASE_NAME` (optional): The name you want your KeePass file to have. If not set, it will default to `bitwarden.kdbx`.
- `BITWARDEN_URL` (optional): A custom Bitwarden/Vaultwarden instance. If you are using the official https://bitwarden.com, you can leave this blank.

### Backup location

All backups will be written to `/exports`. You need to mount that volume locally in order to retrieve the backup file.

### Minimal Docker command

In your terminal, run:

```sh
$ docker run --rm -it -v ./exports:/exports rogsme/bitwarden-to-keepass
```

**The `--rm --it` is important!** Why?
- `--rm`: The Docker container will delete itself after it runs. This ensures no config leaking.
- `-it`: The script will ask for your credentials, so Docker has to run interactively.

First, the script will ask for your Keepass DB password. The input is hidden, so it won't be visible on your terminal:

``` sh
$ DATABASE_PASSWORD is not set
$ Keepass DB password [input is hidden]
```

Then, your Bitwarden username:

``` sh
$ Email address: your@email.com
```

Then, your master password. The input is hidden, so it won't be visible on your terminal:

``` sh
$ Master password: [input is hidden]
```

Finally, if you have 2FA enabled, it will ask for your 2FA code:

``` sh
$ Two-step login code: 123456
```

And it'll start converting your passwords into KeePass! You'll see something similar to this:

``` sh
Generating KeePass file /exports/bitwarden.kdbx
2024-02-20 15:12:54 :: INFO :: KeePass database does not exist, creating a new one.
2024-02-20 15:13:20 :: INFO :: Folders done (1).
2024-02-20 15:13:36 :: INFO :: Starting to process 999 items.
2024-02-20 15:13:36 :: INFO :: Saving changes to KeePass database.
2024-02-20 15:13:43 :: INFO :: Export completed.
```

In the end, the script will lock your vault and log out of your account:

``` sh
Your vault is locked.
You have logged out.
KeePass file /exports/bitwarden.kdbx generated successfully
```

And you can find your file in your mounted directory!

``` sh
$ ls exports
bitwarden.kdbx
```

## FAQ

- Why can't I keep my session open?

  Basically, for security reasons. I prefer the Docker container to ask for my credentials each time and not save them.
