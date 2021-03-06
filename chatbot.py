import re
import telebot
import servicio
import logging
from config import BOT_TELEGRAM_URI

bot = telebot.TeleBot(BOT_TELEGRAM_URI)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

ERROR_MSJ = '¡Lo siento! Hubo un error inesperado *~*'

def start():
	bot.polling()

@bot.message_handler(commands=['info','add','rm','get','getc','top','tail','build'])
def command(message):
	texto = message.text.lower().strip().split(' ')
	d =  {'comando': texto[0].replace('/', ''), 'args': [x for x in texto[1:] if len(x) > 0] if len(texto) > 1 else None}
	print('INPUT:',d)
	if d['comando']=='info':
		bot.reply_to(message, info(d['args']))
	elif d['comando']=='add':
		bot.reply_to(message, add(d['args']))
	elif d['comando']=='rm':
		bot.reply_to(message, rm(d['args']))
	elif d['comando']=='get':
		bot.reply_to(message, get(d['args']))
	elif d['comando']=='getc':
		bot.reply_to(message, getc(d['args']))
	elif d['comando']=='top':
		bot.reply_to(message, top(d['args']))
	elif d['comando'] == 'tail':
		bot.reply_to(message, tail(d['args']))
	elif d['comando'] == 'build':
		bot.reply_to(message, build())
	else: bot.reply_to(message, info())


def info(args=None):
	comando = args[0] if args else None
	if comando=='add':
		return "/add" \
			   "\nArgumentos (obligatorios): url del sitio" \
			   "\nDescripción: lee, clasifica y guarda en tu biblioteca el artículo indicado" \
			   "\nUso: /add {url}. Ejemplo: /add https://towardsai.net/p/data-science/the-beginners-guide-to-elasticsearch"
	if comando=='rm':
		return "/rm" \
			   "\nArgumentos (obligatorios): id del artículo" \
			   "\nDescripción: elimina de tu biblioteca el artículo indicado" \
			   "\nUso: /rm {id}. Ejemplo: /rm 6236da13c87f5e6139a82c90"
	if comando=='get':
		return "/get" \
			   "\nArgumento (obligatorio): texto a buscar en el título de artículos" \
			   "\nDescripción: busca en tu biblioteca los artículos que coincidan particlal o toalmente con el título del artículo " \
			   "\nUso: /get {titulo}. Ejemplo: /get python para ML"
	if comando=='getc':
		return "/getc" \
			   "\nArgumentos (obligatorios): categorías de artículos" \
			   "\nDescripción: busca en tu biblioteca los artículos que coincidan con las categorías indicadas. Cada categoría debe ir separada por comas" \
			   "\nUso: /getc {categorias}. Ejemplo: /getc python,ml,data"
	elif comando=='top':
		return "/top" \
			   "\nArgumentos (opcionales): número de topicos a listar (predeterminado 10)" \
			   "\nDescripción: obtiene una lista de las categorías y el número de artículos asociados. Ordenados de forma descendente" \
			   "\nUso: /top {numero}. Ejemplo: /top 15"
	elif comando == 'tail':
		return "/tail" \
			   "\nArgumentos (opcionales): número de topicos a listar (predeterminado 10)" \
			   "\nDescripción: obtiene una lista de las categorías y el número de artículos asociados. Ordenados de forma ascendente" \
			   "\nUso: /tail {numero}. Ejemplo: /tail 15"
	elif comando == 'build':
		return "/build" \
			   "\nDescripción: Asigna categorías a cada artículo de la biblioteca. Ignorando las categorías explícitamente excluidas por la variable de configuración CATEGORIAS_EXCLUIR" \
			   "\nUso: /build"
	else: return "/info" \
				 "\nArgumentos (opcionales): 'add', 'rm', 'get', 'top', 'tail'"\
			   "\nDescripción: obtienes informacion cada comando para saber su forma de uso" \
			   "\nUso:/info {argumento}. Ejemplo: /info top"


def add(args):
	if not args: return 'Argumento requerido'
	res = re.search('https?.+$', args[0]) if args else None
	if not res: return 'Lo siento no reconocí una URL válida'
	url = res[0]
	res = servicio.servicio_add(url)
	if not res['ok']: return ERROR_MSJ+'\n'+res['msj']
	return res['msj']

def rm(args):
	if not args: return 'Argumento requerido'
	res = servicio.servicio_rm(args[0])
	if not res['ok']: return ERROR_MSJ + '\n' + res['msj']
	return res['msj']

def get(args):
	if not args: return 'Argumento requerido'
	res = servicio.servicio_get(args[0])
	if not res['ok']: return ERROR_MSJ + '\n' + res['msj']
	return res['msj']

def getc(args):
	if not args: return 'Argumento requerido'
	res = servicio.servicio_getc(args[0].split(','))
	if not res['ok']: return ERROR_MSJ + '\n' + res['msj']
	return res['msj']

def top(args):
	parametro = args[0] if args else '10'
	parametro = servicio.try_generic(int, parametro) if parametro else None
	if parametro == None or (parametro != None and parametro < 0): return 'Argumento inválido'
	parametro = parametro if parametro > 0 else 10
	res = servicio.servicio_top(parametro)
	if not res['ok']: return ERROR_MSJ + '\n' + res['msj']
	return res['msj']

def tail(args):
	parametro = args[0] if args else '10'
	parametro = servicio.try_generic(int, parametro) if parametro else None
	if parametro == None or (parametro != None and parametro < 0): return 'Argumento inválido'
	parametro = parametro if parametro > 0 else 10
	res = servicio.servicio_top(parametro,False)
	if not res['ok']: return ERROR_MSJ + '\n' + res['msj']
	return res['msj']

def build():
	res = servicio.servicio_build()
	if not res['ok']: return ERROR_MSJ + '\n' + res['msj']
	return res['msj']



if __name__ == '__main__': start()
