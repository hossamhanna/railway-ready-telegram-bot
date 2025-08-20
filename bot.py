import asyncio, secrets
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.config import BOT_TOKEN
from app.db import init_db, SessionLocal
from app.models import User
from sqlalchemy import select

bot = Bot(BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher()

def main_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='💰 الرصيد', callback_data='balance'),
         InlineKeyboardButton(text='🧾 شحن', callback_data='deposit')],
        [InlineKeyboardButton(text='🧩 المهام', callback_data='tasks'),
         InlineKeyboardButton(text='💵 سحب', callback_data='withdraw')],
        [InlineKeyboardButton(text='👥 الدعوات', callback_data='invite'),
         InlineKeyboardButton(text='⭐ VIP', callback_data='vip')],
    ])
    return kb

async def get_or_create_user(tg_id:int, username:str|None, ref_param:str|None):
    async with SessionLocal() as s:
        q = await s.execute(select(User).where(User.tg_id==tg_id))
        u = q.scalar_one_or_none()
        if u: return u
        ref_code = secrets.token_hex(3)
        referred_by = None
        if ref_param:
            q2 = await s.execute(select(User).where(User.ref_code==ref_param))
            owner = q2.scalar_one_or_none()
            if owner: referred_by = owner.id
        u = User(tg_id=tg_id, username=username, ref_code=ref_code, referred_by=referred_by)
        s.add(u); await s.commit(); await s.refresh(u)
        return u

@dp.message(F.text.startswith('/start'))
async def start(m: Message):
    parts = m.text.strip().split(maxsplit=1)
    ref = parts[1] if len(parts)==2 else None
    user = await get_or_create_user(m.from_user.id, m.from_user.username, ref)
    bot_info = await bot.get_me()
    text = (f"مرحبًا <b>{m.from_user.full_name}</b>!\n"
            f"رصيدك: <b>${user.balance_cents/100:.2f}</b>\n"
            f"كود الدعوة: <code>{user.ref_code}</code>\n"
            f"رابطك: https://t.me/{bot_info.username}?start={user.ref_code}")
    await m.answer(text, reply_markup=main_kb())

@dp.callback_query(F.data=='balance')
async def cb_balance(cq):
    async with SessionLocal() as s:
        q = await s.execute(select(User).where(User.tg_id==cq.from_user.id))
        user = q.scalar_one_or_none()
        if not user:
            await cq.answer('لم يتم العثور على حسابك.', show_alert=True)
            return
        await cq.message.edit_text(f"رصيدك الحالي: <b>${user.balance_cents/100:.2f}</b>", reply_markup=main_kb())
        await cq.answer()

async def on_startup():
    await init_db()

if __name__ == '__main__':
    asyncio.run(on_startup())
    dp.run_polling(bot)