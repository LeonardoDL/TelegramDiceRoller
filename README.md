# TelegramDiceRoller

I made a bot for Telegram that allows you to make more complex rolls than the standard Roll'emBot.</br>
The bot might still have a few bugs because I didn't spend that much time debugging it, so use it on your own risk.</br>
You can copy the code to your machine, generate a new bot_id with bot father and create your own diceBot.

#### Explaining the roll command:

Use 'xdy' to roll x y-sided dice and sum their values. 'dy' rolls 1 y-sided die.</br>
<b>Ex:</b> '/roll 2d6' will roll 2 6-sided dice.

Use 'l'/'L' or 'h'/'H' to refer to the lowest or highest rolls of a set respectively</br>
<b>Ex:</b> '/roll 2d6-H' will roll 2 6-sided dice and remove the highest value.

You can make operations like '+', '-', '*' and '/'</br>
<b>Ex:</b> '/roll 2d6+1d8 \* 1d4' will roll 2 6-sided dice, sum their values, then roll 1 8-sided die and 1 4-sided die, multiply the last 2 results and sum with the 2d6 result.

You can nest expressions. Parenthesis are optional (but sometimes they change the priorities) and die operations have the highest priority.</br>
<b>Ex:</b> '/roll 1d6d8' will roll 1d6 and roll d8's equal to the result of the 1d6.</br>
<b>Ex:</b> '/roll 1d(6d8)' will roll 6d8 and then take the result to make '1d(result)'</br>
<b>Ex:</b> '/roll 1+2*1d6' will roll first, then multiply and then sum.

'L' and 'H' always refers to the last set of rolls.</br>
<b>Ex:</b> In '/roll 2d6d4-H' the H refers to a dice in the roll of the d4s and not the d6s.

The bot can't handle negatives and float numbers. Any negative rolls return 0. Float values are floored.</br>
<b>Ex:</b> '/roll 1d(0-2)' will result in rolling a 1d(-2) and 0 as result.</br>
<b>Ex:</b> '/roll 1d(5/2)' will result in rolling a 1d(2.5) that becomes 1d2.
