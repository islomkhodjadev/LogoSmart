

API_TOKEN = '6849270629:AAG7aM98gGmp95LoAy1TooJBCvkACu3NSOk'
import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters.command import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import logging



# Initialize bot and storage
session = AiohttpSession()
bot = Bot(token=API_TOKEN, session=session)
storage = MemoryStorage()

# Define states
class Form(StatesGroup):
    name = State()
    like_bots = State()
    language = State()

# Initialize router and dispatcher
router = Router()
dp = Dispatcher(storage=storage)

# Start command handler
@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.name)
    await message.answer("Salom ismingiz nima?", reply_markup=ReplyKeyboardRemove())

# Handler to process name
@router.message(Form.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Form.like_bots)
    
    # Define the keyboard layout
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton("Yes"), KeyboardButton("No"))
    
    await message.answer(f"Nice to meet you, {message.text}! Do you like to write bots?", reply_markup=markup)
# Handler for liking bots
@router.message(Form.like_bots)
async def process_like_bots(message: Message, state: FSMContext) -> None:
    if message.text.lower() in ["yes", "no"]:
        await state.update_data(like_bots=message.text.lower())
        await state.set_state(Form.language)
        await message.answer("What programming language do you use?", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Please answer with 'Yes' or 'No'.")

# Handler for programming language
@router.message(Form.language)
async def process_language(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['language'] = message.text
    await state.clear()  # Clear state after collecting all data
    await message.answer(f"Got it! You said your name is {data['name']}, you {'like' if data['like_bots'] == 'yes' else 'don\'t like'} to write bots, and you use {data['language']}.")

async def main():
    # Include router into dispatcher
    dp.include_router(router)

    # Start polling
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
