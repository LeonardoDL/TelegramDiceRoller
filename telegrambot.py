# -*- coding: UTF8 -*-
import requests
import datetime
import re
from sentence import OrderLulException
from sentence import TooManyVarsException
from compiler import DiceCompiler

class BotHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    #url = "https://api.telegram.org/bot<token>/"

    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_first_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[0]
        else:
            last_update = None

        return last_update


token = '1026926157:AAHPESTZ8flyFuCvFzoJWFCACoji3i4Eh9Y' #Token of your bot
dice_bot = BotHandler(token) #Your bot's name

def main():
    new_offset = 0
    print('hi, now launching...')

    while True:
        all_updates=dice_bot.get_updates(new_offset)

        if len(all_updates) > 0:
            for current_update in all_updates:
                print("Total: " + str(len(all_updates)))
                print(current_update)
                first_update_id = current_update['update_id']
                first_chat_text=""
                first_chat_id=""
                first_chat_name=""
                try:
                    if 'text' not in current_update['message']:
                        first_chat_text='New member'
                    else:
                        first_chat_text = current_update['message']['text']
                    first_chat_id = current_update['message']['chat']['id']
                    if 'first_name' in current_update['message']:
                        first_chat_name = current_update['message']['chat']['first_name']
                    
                    elif 'new_chat_member' in current_update['message']:
                        first_chat_name = current_update['message']['new_chat_member']['username']
                    
                    elif 'reply_to_message' in current_update['message']:
                        first_chat_name = current_update['message']['from']['first_name']
                        new_offset = first_update_id + 1
                        continue
                    
                    elif 'from' in current_update['message']:
                        first_chat_name = current_update['message']['from']['first_name']
                    
                    else:
                        first_chat_name = "unknown"
                        new_offset = first_update_id + 1
                        continue
                
                except KeyError:
                    print("\n\nGot it!")


#---------------------------------------------------------------------------------------------------------------------------------
                
                if first_chat_text.startswith("/start"):
                    first_chat_text = first_chat_text[61:]
                    new_offset = first_update_id + 1
                    continue

                elif first_chat_text.startswith("/guide"):
                    first_chat_text = first_chat_text[6:]
                    dice_bot.send_message(first_chat_id, "<b>Use 'xdy' to roll x y-sided dice and sum their values. 'dy' rolls 1 y-sided die.</b>\n" + \
                                                          "Ex: '/roll 2d6' will roll 2 6-sided dice.\n\n" + \
                                                          "<b>Use 'L' or 'H' to refer to the lowest or highest rolls of a set respectively</b>\n" + \
                                                          "Ex: '/roll 2d6-H' will roll 2 6-sided dice and remove the highest value.\n" + \
                                                          "Ex: '/roll 4d6-4H' will roll 4 6-sided dice and remove the 4 highest ones.\n\n" + \
                                                          "<b>You can make operations like '+', '-', '*' and '/'</b>\n" + \
                                                          "Ex: '/roll 2d6+1d8*1d4' will roll 2 6-sided dice, sum their values, then roll 1 8-sided die and 1 4-sided die, multiply the last 2 results and sum with the 2d6 result\n\n" + \
                                                          "<b>You can nest expressions. Parenthesis are optional (but sometimes they change the priorities) and die operations have the highest priority.</b>\n" + \
                                                          "Ex: '/rol 1d6d8' will roll 1d6 and roll d8's equal to the result of the 1d6.")
                    new_offset = first_update_id + 1
                    continue
                elif first_chat_text.startswith("/help"):
                    first_chat_text = first_chat_text[6:]
                    dice_bot.send_message(first_chat_id, "/roll  Rolls a die\n" + \
                                                          "/guide  Explanation of the syntax\n" + \
                                                          "/help  Lists all commands")
                    new_offset = first_update_id + 1
                    continue

                elif first_chat_text.startswith("/roll "):
                    first_chat_text = first_chat_text[6:]
                    if not ("d" in first_chat_text or "D" in first_chat_text):
                        dice_bot.send_message(first_chat_id, "You're not rolling any dice buddy. Use 'd' or 'D' to represent dice.")
                        new_offset = first_update_id + 1
                    else:
                        compiler = DiceCompiler(doPrint=False)
                        compiler.CompileSentence(first_chat_text)

                        if compiler.stop:
                            if compiler.message == "":
                                print("Error! Program could'nt parse given input\n")
                                dice_bot.send_message(first_chat_id, "Error! Program could'nt parse given input")
                            else:
                                dice_bot.send_message(first_chat_id, "Error! " + compiler.message)
                            new_offset = first_update_id + 1
                        elif compiler.code != "":
                            print("Error! Program stopped before consuming all input! = '" + compiler.code + "'\n")
                            dice_bot.send_message(first_chat_id, "Error! Program stopped before consuming all input!")
                            new_offset = first_update_id + 1
                        else:
                            #dice_bot.send_message(first_chat_id, 'Your sentence is actually valid!')
                            #new_offset = first_update_id + 1

                            #if current_update['message']['from']['username'] == 'LeonardoDelLama':
                            print("\n")
                            try:
                                acc = compiler.sentence.process(1)
                                print("This is the output\n " + compiler.sentence.out)
                                if compiler.sentence.out != '' and compiler.sentence.out[-1] != '\n':
                                    compiler.sentence.out += '\n'
                                if len(compiler.sentence.out) > 1000:
                                    dice_bot.send_message(first_chat_id, "Too many calculations to show\n" + "= " + str(acc))
                                else:
                                    dice_bot.send_message(first_chat_id, "Resolving: " + first_chat_text + "\n" + compiler.sentence.out + "= " + str(acc))
                                new_offset = first_update_id + 1
                            except OrderLulException as ole:
                                dice_bot.send_message(first_chat_id, "Error: Variable '" + ole.var + "' mentions a dice roll that doesn't exist")
                                new_offset = first_update_id + 1
                            except TooManyVarsException:
                                dice_bot.send_message(first_chat_id, "Error: There are more variables than dice rolls")
                                new_offset = first_update_id + 1
                else:
                    new_offset = first_update_id + 1
                    continue

#---------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()