CONFIG = {
    # Don't forget to remove the old database (flags.sqlite) before each competition.

    # The clients will run sploits on TEAMS and
    # fetch FLAG_FORMAT from sploits' stdout.

    # WARNING: THIS IS A FALLBACK DICTIONARY IF THE PROTOCOL DOES NOT PROVIDE UPDATED TEAMS.
    'TEAMS': {'Team #{}'.format(i): '10.10.{}.1'.format(i) for i in range(1, 80 + 1)},

    # Regex per flag di 31 caratteri [A-Z0-9] seguiti da =
    'FLAG_FORMAT': r'[A-Z0-9]{31}=',

 
    'SYSTEM_TOKEN': '4242424242424242',
    # This configures how and where to submit flags.
    # The protocol must be a module in protocols/ directory.

    'SYSTEM_PROTOCOL': 'ccitTEST',
    'ATTACK_INFO': "http://10.10.0.1:8081/flagIds",
    'ATTACK_INFO_ENDPOINT': "http://10.10.0.1:8081/flagIds",
    'SYSTEM_HOST': '192.168.1.4',#mettere indirizzo gameserver
    'SYSTEM_PORT': 8080,
    'TEAM_TOKEN': 'your_secret_token',
    
    # Limiti di invio: massimo 30 richieste al minuto (1 ogni 2 secondi)
    # Inviamo le flag a blocchi (batch) di 100 per efficienza.
    'SUBMIT_FLAG_LIMIT': 100,
    'SUBMIT_PERIOD': 2,
    
    # Le flag sono valide per 5 round (10 minuti)
    'FLAG_LIFETIME': 10 * 60,

    # Password per l'interfaccia web del farm
    'SERVER_PASSWORD': 'cyberchallenge',

    # API Auth per i client che inviano flag al farm
    'ENABLE_API_AUTH': False,
    'API_TOKEN': '00000000000000000000'
}
