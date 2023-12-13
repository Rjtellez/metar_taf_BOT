import asyncio
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, Updater, CallbackContext
from models.DSM import Insert, Get
from models.NWS import NWS




TOKEN: Final = '6503314509:AAEFhETlD0DPTCwDhiSG9XlrpCLFaTjsDtM'
BOT_USERNAME: Final = '@RJTG_metarbot'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text('Hello, if you need any METAR report, please send the ICAO codes, separated by comma like this:\nMMMX,MMGL,MMEP,MMM27,MMMZP\n\n Or if you need to upload a METAR report, please send the command "CARGAR" followed by the METAR report like this:\nCARGAR METAR MMM27 301515Z 00000KT 7SM FEW030 19/12 A3010 RMK 8/100')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text('If you need help, please contact the developer: @RJTellezGarcia')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text('Custom command')

timers = {}

#Responses
def handle_response(text: str) -> str:
  text = text.upper()
  if text.startswith('CARGAR'):
    text = text.replace('CARGAR ', '')
    metar = text.upper()
    if metar.startswith('METAR '):
      metar = metar.replace('METAR ', '')
    else:
      metar = metar
    insert = Insert()
    insert.insert_metar(metar)
    response = 'METAR report has been uploaded correctly' + ' ' + metar
    return response
    
  else:
    processed: str = text.upper()
    processed = processed.replace(" ","").split(",")
    metars = []
    nws = NWS()
    dsm_get = Get() 
    print(processed)
    for des in processed:

      if len(des) == 5:
        metar = dsm_get.get_last(des)[0]
        metars.append(metar)
      else:
          metar = nws.get_last_metar(id=des)["metar"].message.replace("\n", "")
          metars.append(metar)
    
    return metars

# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#   message_type: str = update.message.chat.type
#   text: str = update.message.text
#   print(f'User({update.message.chat.id}) in {message_type}: "{text}"')

#   if message_type == 'group':
#     if BOT_USERNAME in text:
#       new_text: str = text.replace(BOT_USERNAME,'').strip()
#       response: str = handle_response(text)
#     else:
#       return
#   else:
#     response: str = handle_response(text)

#   print('Bot:', response)
#   if len(response[0]) == 1:
#     metars_text = response
#   else:
#     metars_text = "\n\n".join(response)
#   # metars_text = "\n\n".join(response)
#   await update.message.reply_text(metars_text)
   
  
  # await update.message.reply_text(response)
tasks = {}

async def handle_message(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    message_type = update.message.chat.type
    text = update.message.text
    print(f'User({chat_id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, '').strip()
            response = handle_response(text)
        else:
            return
    else:
        response = handle_response(text)

    print('Bot:', response)
    if len(response[0]) == 1:
        metars_text = response
    else:
        metars_text = "\n\n".join(response)

    await update.message.reply_text(metars_text)

    # Cancelar la tarea existente si hay una
    if chat_id in tasks:
        tasks[chat_id].cancel()

    # Crear una nueva tarea para reiniciar la comunicación después de cierto tiempo
    tasks[chat_id] = asyncio.create_task(restart_communication(chat_id, context))

async def restart_communication(chat_id, context):
    # Resto del código...:
    await asyncio.sleep(3800) 
    # Esta función se llama cuando expira la tarea
    del tasks[chat_id]
    #await app.send_message(chat_id, "La conversación ha expirado. Por favor, inicie una nueva.")
    await context.bot.send_message(chat_id, "La conversación ha expirado. Por favor, inicie una nueva.")

    # Puedes realizar cualquier otra acción de reinicio aquí, si es necesario

# Resto del código...

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
  print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
  print('Starting bot...')
  app =  Application.builder().token(TOKEN).build()

  #commands
  app.add_handler(CommandHandler('start', start_command))

  app.add_handler(CommandHandler('help', help_command))
  app.add_handler(CommandHandler('custom', start_command))

  #messages
  app.add_handler(MessageHandler(filters.TEXT, handle_message))

  #errors
  app.add_error_handler(error)
  print('Polling...')
  app.run_polling(poll_interval=3, timeout=180)
  