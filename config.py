
# GENERALES
# N_TOPICOS_LIMITE: indica la cantidad máxima de artículos que puedes tener en tu biblioteca
LIMITE_MAX_ARTICULOS = 200
# CATEGORIAS_EXCLUIR: indica las categorías que NO se tomarán en cuenta al generar el modelo LDA de cada artículo
CATEGORIAS_EXCLUIR = []

# CHATBOT
# BOT_TELEGRAM_URI: token de conexión con el chatbot de Telegram
BOT_TELEGRAM_URI = ''

# Nombre de la BD
BD = 'topic_modeling'
# Nombre de la colección de la BD
COLLECTION = 'articulos'
# MONGO_URI: cadena de conexión a la base de datos de MongoDB
MONGO_URI='mongodb://usuario:pass@127.0.0.1:27017/{}'.format(BD)