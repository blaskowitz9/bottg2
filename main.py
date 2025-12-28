from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)

# Bot token from environment variables
TOKEN = os.getenv('BOT_TOKEN', '7873185866:AAEL01wlssfoU6_UDl_WhdisyNFjPw4gkYM')

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Channel ID for subscription check
CHANNEL_ID = '-1003584613132'

@dp.message(Command('start'))
async def start_command(message: types.Message):
    """Handler for the /start command"""
    await message.answer('Hello! I am a bot that will check your subscription to the channel.')
    await check_subscription(message)

@dp.message()
async def handle_all_messages(message: types.Message):
    """Handler for all messages to check subscription"""
    await check_subscription(message)

async def check_subscription(message: types.Message):
    """Check user's subscription to the channel"""
    try:
        # Get user status in the channel
        user_status = await bot.get_chat_member(
            chat_id=CHANNEL_ID, 
            user_id=message.from_user.id
        )
        
        # Check that the user hasn't left the channel
        if user_status.status not in ['left', 'kicked']:
            await message.answer('You are subscribed to the channel, you can receive content!')
            await send_content(message)
        else:
            # Create subscription button
            markup = types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(
                    text='Subscribe to the channel', 
                    url='https://t.me/PlantsvsZombiesFusionLegend'
                )],
                [types.InlineKeyboardButton(
                    text='Check subscription', 
                    callback_data='check_subscription'
                )]
            ])
            
            await message.answer(
                'To receive content, you must subscribe to the channel!',
                reply_markup=markup
            )
    
    except Exception as e:
        logging.error(f"Error checking subscription: {e}")
        await message.answer('An error occurred while checking your subscription. Please try again later.')

@dp.callback_query(lambda callback: callback.data == 'check_subscription')
async def check_subscription_callback(callback: types.CallbackQuery):
    """Handler for subscription check button click"""
    try:
        # Get user status in the channel
        user_status = await bot.get_chat_member(
            chat_id=CHANNEL_ID, 
            user_id=callback.from_user.id
        )
        
        # Check that the user hasn't left the channel
        if user_status.status not in ['left', 'kicked']:
            await callback.message.answer('You are subscribed to the channel, you can receive content!')
            await send_content(callback.message)
            await callback.answer('✅ Subscription confirmed!')
        else:
            # Create subscription button
            markup = types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(
                    text='Subscribe to the channel', 
                    url='https://t.me/fusionlegend/2'
                )],
                [types.InlineKeyboardButton(
                    text='Check subscription', 
                    callback_data='check_subscription'
                )]
            ])
            
            await callback.message.answer(
                'You are not subscribed to the channel yet! Please subscribe and click "Check subscription" again.',
                reply_markup=markup
            )
            await callback.answer('❌ You are not subscribed to the channel!')
    
    except Exception as e:
        logging.error(f"Error checking subscription: {e}")
        await callback.message.answer('An error occurred while checking your subscription. Please try again later.')
        await callback.answer('⚠️ An error occurred!')

async def send_content(message: types.Message):
    """Send content to the user"""
    # Here you can add various content
    content_messages = [
        "🎉 Here is your promo code for the Nyan Cat Sunflower skin - TGSKIN245",
        "✅ Enter the promo code in the Shop!"
    ]
    
    for msg in content_messages:
        await message.answer(msg)

async def main():
    """Main function to start the bot"""
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())