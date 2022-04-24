import os
import os.path
import glob
from telegram import *
from telegram.ext import *
from urllib.request import urlopen
from settings import *
import time
import json
from datetime import datetime

###########################

def start(update, context):
  user=str(update.message.from_user.id)  
  group=str(update.message.chat_id)
  groupu=f"@{update.message.chat.username}"
  Bchat="-0123456789"
  Bcid="@none"
  if str(update.message.chat.type) == "private":
    update.message.reply_text(f"انا بوت احظر اي قناة تتكلم بلكروب \n ضيفني بكروبك و ارفعني ادمن ونطيني صلاحيات الحظر و الحذف \n بعدها ارسل /start بلكروب حتى يبدئ البوت بلعمل \n\n\n لمزيد من المعلومات اضغط /help", parse_mode='markdown')
  else:
   try:
     adm=context.bot.getChatMember(chat_id=update.message.chat_id, user_id=user).status
     print(adm)
     if str(adm) == "creator" or str(adm) == "administrator":
         if os.path.isfile(f"{group}_ban_appr_lists.txt") and os.path.isfile(f"{group}_ban_appr_lists.txt"):
            update.message.reply_text("`البوت شغال`", parse_mode='markdown')
         else:
          try:
            Lchat=str(context.bot.get_chat(update.message.chat_id).linked_chat_id)
            Lcid=str(context.bot.getChat(Lchat).username)
            Lcid=f"@{Lcid}"
            if not Lchat:
              Lchat="-0123456789"
          except:
               Lchat="-0123456789"
               Lcid="@none"
          dict_grp={
    groupu: {
   "approved_chats": {
     group: groupu,
     Lchat: Lcid     
   },
   "banned_chats": {
    Bchat: Bcid
   }
 }
}
          print(dict_grp)
          with open(f"{group}_ban_appr_lists.txt", 'w+') as f:
              json.dump(dict_grp, f, indent=4, sort_keys=True)
          update.message.reply_text("✅ *البوت يعمل الان*", parse_mode='markdown')
          try:
             kk=context.bot.getChat(Lchat).username
             print(f"\n\nمعلومات البدء:\nاسم المجموعة = @{update.message.chat.username}\nمعرف المجموعة = @{kk}\n\n")
          except:
           try:
             print(f"\n\nمعلومات البدء:\nاسم المجموعة = @{update.message.chat.username}\nرابط المجموعة = مجموعة خاصة\n\n")
           except:
            pass
   except:
     update.message.reply_text("`السلام عليكم! \nاستطيع حظر القنواة اللتي ترسل رسائل في مجموعتك\nلا تعرف طريقة الاستخدام؟\nاضغط /help.`", parse_mode='markdown')
     pass
def help(update, context):
  if str(update.message.chat.type) == "private":
     update.message.reply_text(f"""- أضفني إلى المجموعة ، وامنح حقوق المسؤول (حظر المستخدمين وحذف الرسائل على الأقل)
   and `/start` لتشغيل البوت\n
- `/approvechat` <رد لرسالة / اسم المستخدم أو معرف القناة> :-
   _للموافقة على معرف قناتك (حتى تتمكن من الدردشة عبر قناتك)_\n
- `/disapprovechat` <رد على الرسالة / معرف القناة> :-
   _لحظر / تعطيل / منع معرف القناة المحدد_\n
- `/mychannel` :- 
  _ للحصول على معلومات قناتك المرتبطة_\n
- `/list (الموافق | المحظورين)`:-
  _للحصول على قائمة القنواة الموافقة / المحظورة_ \n
- `/help` :-
   _لإظهار نص المساعدة هذا_\n
*لا يمكن للمسؤولين المجهولين تنفيذ أوامر البوت
 يجب أن تكون ادمن أو مالكًا للمجموعة*""", 
parse_mode='markdown')
  else:
     update.message.reply_text("راسلني خاص للمساعدة", reply_markup=InlineKeyboardMarkup(
                 [
                   [
                     InlineKeyboardButton(
                     text=f"اضغط هنا",
                     url=f"http://t.me/DECSHELLbot"
                      )
                   ]
                 ]
                 ))        

def appr_ban_list(update, context):
  user=str(update.message.from_user.id)
  listc=[]
  num=0
  
  adm=context.bot.getChatMember(chat_id=update.message.chat_id, user_id=user).status
  if adm == "creator" or adm == "administrator":
      if "الموافق" in update.message.text.split(' '):
        group=str(update.message.chat_id)
        groupu=f"@{update.message.chat.username}"
        with open(f"{group}_ban_appr_lists.txt", 'r') as f:
                 obj=json.load(f)
        Nlists=obj[f"{groupu}"]['approved_chats']
        for i in Nlists:                                                     
            word=Nlists[i]
            num += 1
            listc.append(f"""{num}) `{i}`\n     *{word}*""")
            listch='\n'.join(listc)
        update.message.reply_text(f"""*معرفات القنوات الموافق عليها*:-\n{listch}""", parse_mode='MARKDOWN')
      elif "المحظورين" in update.message.text.split(' '):
        group=str(update.message.chat_id)
        groupu=f"@{update.message.chat.username}"
        with open(f"{group}_ban_appr_lists.txt", 'r') as f:
                 obj=json.load(f)
        Nlists=obj[f"{groupu}"]['banned_chats']
        for i in Nlists:                                                     
            word=Nlists[i]
            num += 1
            listc.append(f"""{num}) `{i}`\n     *{word}*""")
            listch='\n'.join(listc)
        update.message.reply_text(f"""*معرفات القنوات المحظورة*:-\n{listch}""", parse_mode='MARKDOWN')
      else:
         update.message.reply_text("خطأ! \n عليك كتابة اما \n `/list الموافق` \n او `/list المحظورين`")
def approve_channel(update, context):
  user=str(update.message.from_user.id)
  adm=context.bot.getChatMember(chat_id=update.message.chat_id, user_id=user).status
  if adm == "creator" or adm == "administrator":
   try:
     print(adm)
     Lcid=None
     group=str(update.message.chat_id)
     groupu=f"@{update.message.chat.username}"
     try:
       Lcid=str(update.message.reply_to_message.sender_chat.id)
       Lchat=str(update.message.reply_to_message.sender_chat.username)
     except:
      msg=str(update.message.text.split(' ')[1])
      if msg.startswith("@"):
       try:
         Lcid=str(context.bot.getChat(update.message.text.split(' ')[1]).id)
         Lcm=str(update.message.text.split(' ')[1]) 
         Lchat=Lcm.replace('@', '')
       except:
          pass
      elif msg.startswith("-100"):
       try:
         Lchat=str(context.bot.getChat(update.message.text.split(' ')[1]).username)
         Lcid=str(update.message.text.split(' ')[1])   
       except:
        pass
      if Lcid:
       try:
           url=(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/unbanChatSenderChat?chat_id={update.message.chat_id}&sender_chat_id={Lcid}")
           with urlopen(url) as f:
               update.message.reply_text("موجود")      
           with open(f"{group}_ban_appr_lists.txt", 'r') as f:
                 obj=json.load(f)
           obj[f"{groupu}"]['approved_chats'][f"{Lcid}"]=f'''@{Lchat}'''
           print(obj)
           with open(f"{group}_ban_appr_lists.txt", 'w') as f:
                json.dump(obj, f, indent=4, sort_keys=True) 
       except:         
           with open(f"{group}_ban_appr_lists.txt", 'r') as f:
                 obj=json.load(f)
           obj[f"{groupu}"]['approved_chats'][f"{Lcid}"]=f'''@{Lchat}'''
           print(obj)
           with open(f"{group}_ban_appr_lists.txt", 'w') as f:
                json.dump(obj, f, indent=4, sort_keys=True) 
           update.message.reply_text("تم اضافته في قائمة القنواة الامنة")      
      else:
        update.message.reply_text("لم يتم العثور على الدردشة!")
   except:
          update.message.reply_text("يرجى كتابة سبب الحظر")
           
def disapprove_channel(update, context):
  user=str(update.message.from_user.id)
  adm=context.bot.getChatMember(chat_id=update.message.chat_id, user_id=user).status
  if adm == "creator" or adm == "administrator":
     group=update.message.chat_id
     groupu=f"@{update.message.chat.username}"
     id="doesnt_exist"
     error_msg="يبدو أنه ليس معرف قناة صالحًا ! اعد المحاولة" 
     try:
       msg=update.message.text.split(' ')[1]
       if msg.startswith('-100'):
          id=str(update.message.text.split(' ')[1])   
       elif msg.startswith('@'):
          id=str(context.bot.getChat(update.message.text.split(' ')[1]).id)
       elif update.message.reply_to_message:
          id=str(update.message.reply_to_message.sender_chat.id)
     except Exception as e:
         if str(e) == "فهرس القائمة خارج النطاق":
          error_msg="يجب كتابة السبب !"
     if id.startswith('-100'):
      try:
        url=(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/banChatSenderChat?chat_id={update.message.chat_id}&sender_chat_id={id}")
        with urlopen(url) as f:
          update.message.reply_text("محظور !")
      except:
        pass
      try:
                with open(f"{group}_ban_appr_lists.txt", 'r') as f:
                     obj=json.load(f)
                sobj=obj[f"{groupu}"]['approved_chats']   
                del obj[f"{groupu}"]['approved_chats'][f"{id}"]
                with open(f"{group}_ban_appr_lists.txt", 'w+') as q:
                  json.dump(obj, q, indent=4, sort_keys=True)
      except:
        pass
     else:
      update.message.reply_text(error_msg)         
def ban_channel_updates(update, context):
 if update.message.sender_chat:
  id=str(update.message.sender_chat.id)
  group=str(update.message.chat_id)
  pp=[]
  pe=[]
  groupu=f"@{update.message.chat.username}"
  if os.path.isfile(f"{group}_ban_appr_lists.txt"):
   if id.startswith('-100') or id in '777000':
    if str(context.bot.get_chat(update.message.chat_id).linked_chat_id) == id:
       pass
    if str(update.message.chat_id) == id:
       pass
    else:
      try:
        with open(f"{group}_ban_appr_lists.txt", 'r') as f:
                 obj=json.load(f)
        Nlists=obj[f"{groupu}"]['approved_chats']
        for name in Nlists:
          pe.append(name)
        if id in pe:
           pass
        else:
          try:
            context.bot.delete_message(chat_id=update.message.chat_id,
               message_id=update.message.message_id)
            url=(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/banChatSenderChat?chat_id={update.message.chat_id}&sender_chat_id={update.message.sender_chat.id}")
            with urlopen(url) as f:
                print(f" ")
            try:
             with open(f"{group}_ban_appr_lists.txt", 'r') as f:
                 obj=json.load(f)
             Nlists=obj[f"{groupu}"]['banned_chats']
             for name in Nlists:
                pp.append(name)
             if id in pp:
               pass
             else:
                bunned=context.bot.send_message(chat_id=update.message.chat_id, 
                          reply_to_message_id=None,
                parse_mode='markdown',
                text=f"تم حظر احدى القنواة اللتي ارادت ان تتكلم وتم حذف رسالتها")
                with open(f"{group}_ban_appr_lists.txt", 'r') as f:
                     obj=json.load(f)
                obj[f"{groupu}"]['banned_chats'][f"{id}"]=f'''@{update.message.sender_chat.username}'''
                with open(f"{group}_ban_appr_lists.txt", 'w') as f:
                    json.dump(obj, f, indent=4, sort_keys=True)
            except:
                pass
          except Exception as e:
              print(str(e))
      except:
         pass

def myChannel(update, context):
  user=str(update.message.from_user.id)
  adm=context.bot.getChatMember(chat_id=update.message.chat_id, user_id=user).status
  if adm == "creator" or adm == "administrator":
   try:
      kk=context.bot.get_chat(update.message.chat_id).linked_chat_id
      uname=context.bot.getChat(kk).username
      update.message.reply_text(f"_المعلومات:_\n*معرفات قنواتك* = `{kk}`\n*username* = @{uname}", parse_mode='markdown')
   except:
     update.message.reply_text("مجموعتك بدون قنوات")
def setup_dispatcher(dp):
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(PrefixHandler('/', 'list', appr_ban_list))
    dp.add_handler(PrefixHandler('/', 'approvechat', approve_channel))
    dp.add_handler(PrefixHandler('/', 'mychannel', myChannel))
    dp.add_handler(PrefixHandler('/', 'disapprovechat', disapprove_channel))
    dp.add_handler(MessageHandler(Filters.chat_type.supergroup, ban_channel_updates))
    return dp
