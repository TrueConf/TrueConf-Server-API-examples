# TrueConf Server API Use Cases

This code sample provides several use cases described in our knowledge base articles and performed using TrueConf Server API::

1. [How to add user accounts from a file](https://trueconf.com/blog/knowledge-base/how-to-add-user-accounts-from-a-file.html)

1. [How to delete past meetings automatically](https://trueconf.com/blog/knowledge-base/how-to-delete-past-meetings-automatically.html)

*Switch to other languages: [Russian](README.ru.md)*

:warning: ***Warning!***
> **We don’t recommend running the script file on an OS with TrueConf Server installed. For this purpose it’s best to use another computer in the local network, which detects the video conferencing server by its IP address or domain name (FQDN).**

The code is written in Python, so you need to take the following steps to get started:

1. Install **Python 3.7+** by downloading it from the official website: https://www.python.org/downloads 

1. Update the **pip** package installer: https://pip.pypa.io/en/stable/installing/#upgrading-pip 

1. Install additional packages for Excel files:

```bash
pip install requests pyexcel pyexcel-odf pyexcel-xls pyexcel-xlsx
```

## Getting ready

[Enable HTTPS](https://trueconf.com/blog/knowledge-base/adjust-https-trueconf-server.html#How_to_set_up_HTTPS_connection) in the TrueConf Server control panel.

Next, go to [API → OAuth2](https://docs.trueconf.com/server/en/admin/web-config#oauth2). Create a new OAuth 2.0 app and check the boxes that are necessary for solving the above tasks:

- conferences
- groups
- groups.users
- users
- users.avatar:read
- users.avatar:write

:point_right: ***Note***
> **Learn more about the OAuth protocol [in TrueConf Server documentation](https://docs.trueconf.com/server/en/admin/web-config#oauth2).**

## Using parameters

You can specify the parameters that are necessary for the script to work in the **data.json** setup file (recommended method) or enter them manually once it has been launched. Here is the list of parameters:

- **`"server"`** – TrueConf Server’s IP address or URL, e.g., **video.company.name** or **10.120.1.10**
- **`"new_users_file"`** – a path to the file with data needed for importing user accounts to the server or deleting them (**.csv**, **.ods**, **.xls** and **.xslx** formats are supported; check this [article on adding users from a file](https://trueconf.com/blog/knowledge-base/how-to-add-user-accounts-from-a-file.html#Step_1_Creating_a_file_for_import))
- **`"client_id"`** – an OAuth app ID
- **`"client_secret"`** – an OAuth app secret key
- **`"delimiter"`** – the separator of values in strings which is needed when using **.csv**; you need to specify the delimiter used in your file
- **`"verify"`** – SSL certificate verification setup that’s necessary when running code on Windows OS (more details at https://requests.readthedocs.io/en/latest/user/advanced/#ssl-cert-verification). If a self-signed SSL certificate is used on the server, it is necessary to download the certificate .crt file on the computer where the script is stored and specify the absolute path to this file in the `"verify"` parameter. If a commercial certificate is used, you need to specify the value **true** without quotes: **`"verify":true`**.

Path to the certificate file:

- TrueConf Server for Linux: `/opt/trueconf/server/etc/webmanager/ssl/ca.crt`
- TrueConf Server for Windows: `C:\Program Files\TrueConf Server\httpconf\ssl\ca.crt`

## Working with the script

**Running the script on Windows**

Go to the directory with the script and run the script with a double click. An alternative way to do it is to open the terminal and run the command `/path/api-examples.py` where `path` is the absolute path to the script.

**Running the script on Linux**

Run this command in the terminal:

```bash
sudo python3 /path/api-examples.py
```

where `path` is the absolute path to the script.

Once the **api-examples.py** script file has been launched, you’ll see the menu in the terminal window where you’ll be prompted to select the required task. To this end, enter one of these commands:

- **S** – reading parameters to connect to the server (from the json.data file or entering them manually)

- **E** – [deleting past meetings](https://trueconf.com/blog/knowledge-base/how-to-delete-past-meetings-automatically.html):
  - Entering the number of days after which you need to delete events (you can set other values, e.g., 1.5 to clear conferences that ended 36 hours before the current time).
  - Getting a list of all stopped conferences.
  - Searching among them for scheduled events with an end date older than the specified one.
  - Deleting conferences.

- **N** – [importing users and groups from a file](https://trueconf.com/blog/knowledge-base/how-to-add-user-accounts-from-a-file.html):
  - Reading data from a file.
  - Adding user groups to the server.
  - Adding accounts.
  - Uploading avatars for users (if specified).
  - Adding users to groups.

- **D** – [deleting users and groups listed in a file](https://trueconf.com/blog/knowledge-base/how-to-add-user-accounts-from-a-file.html#Deleting_data_on_TrueConf_Server);

- **Q** – ending a script.
