# D-Ticket Discord Bot

D-Ticket is a discord bot for ticket management system. This is not final product is currently being in development stay connected for new updates and changes. Also please report if you see any bugs.
### Key Features:-
- Ticket service can be enable or disable.
- Embed Support
- Role support Ticket Manager and Ticket Admin (both have different features)
- Cannot create more then 10 tickets, in-case abuse of more tickets you can change it as you want.

## Installation

Use the package manager [pip](https://pypi.org/project/discord.py/) to install discord.py.

```bash
pip install discord
```

## Usage

Commands:-
```
  - !dttcreate : to be create the ticket
  - !dtclose : to close the ticket (ticket only closed by ticket admin or ticket manager, user just only can make a close request)
  - !tsetadmin : to set a ticket admin with role name 'Ticket Admin' (Ticket Manager can use this command)
  - !tsetmanager : to set a ticket manager with role name 'Ticket Manager' (User with adminstrator permission can use this command)
```
Extra Feature:-
``` 
  - !tservice (extra feature) : you can enable or disable (on/off) ticket service so no one can abuse it by making ticket channels.
  - Ticket channels cannot be create more than 10 ticket channels.

```

## Contributing
Pull requests are welcome, you can discuss for big changes first either creating pull request.
