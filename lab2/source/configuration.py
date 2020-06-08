from source.Entities.user import UsrController
from source.Entities.administrator import Administrator
from source.Entities.MainController import MainController

menu_listing = {
    'Main ui': {
        'register': UsrController.make_register,
        'login': UsrController.make_signin,
        'quit': MainController.looping,
    },
    'User': {
        'Messages stats': UsrController.recieve_stats,
        'Send a message to someone': UsrController.send_a_message,
        'Sign out': UsrController.make_sign_out,
        'Your Inbox': UsrController.inbox_messeges,
    },
    'Admin': {
        'Spamers': Administrator.recieve_spamers,
        'Sign out': MainController.looping,
        'Online': Administrator.recieve_active_users,
        'Events': Administrator.recieve_events,
        'Senders': Administrator.recieve_senders,
    }
}

userRoles = {
    'utilyzer': 'Utilizr ui',
    'admin': 'Admin ui'
}

params = {
    'role': '(admin or utilyzer)'
}
