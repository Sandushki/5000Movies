import discord
from discord.ext import commands
from logic import *
from config import DATABASE, TOKEN

intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)
manager = DB_Manager(DATABASE)

@bot.event
async def on_ready():
    print(f'Bot hazır! {bot.user} olarak giriş yapıldı.')

@bot.command(name='info')
async def info(ctx):
    await ctx.send("""
Kullanabileceğiniz komutlar şunlardır:

!new_movie - yeni bir film eklemek
!movies <LIMIT> - En son yayınlanan filmlerden belirlediğiniz sayı kadar gösterir.
!director <DIRECTOR> - Belirlediğiniz bir film yöneticisinin kaç tane film yaptığını gösterir.
!sql_select <QUERY> - Veri tabanında SQL SELECT sorgusu çalıştırmanızı sağlar. Sorgununun çıktısını size gösterir.
!new_director <DIRECTOR> - Veri tabanına yeni bir film yönetmeni ekler.
""")
    
@bot.command()
async def new_movie(ctx):

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    
    await ctx.send("Lütfen filmin adını girin!")
    name = await bot.wait_for('message', check=check)
    data = [ctx.author.id, name.content]
    
    await ctx.send("Lütfen filmin bütçesini girin.")
    link = await bot.wait_for('message', check=check)
    data.append(link.content)

    await ctx.send("Lütfen filmin 0-150 arasındaki popülerliğini girin.")
    popularity = await bot.wait_for('message', check=check)
    data.append(popularity.content)

    await ctx.send("Lütfen filmin yayın tarihini girin.")
    release_date = await bot.wait_for('message', check=check)
    data.append(release_date.content)

    await ctx.send("Lütfen filmin 0-10 arasındaki değerlendirmesini girin.")
    vote_avg = await bot.wait_for('message', check=check)
    data.append(vote_avg.content)

    await ctx.send("Lütfen filmin kaç kişi tarafından değerlendirildiğini girin.")
    vote_count = await bot.wait_for('message', check=check)
    data.append(vote_count.content)

    await ctx.send("Lütfen filmin kısa özetini girin.")
    overview = await bot.wait_for('message', check=check)
    data.append(overview.content)

    await ctx.send("Lütfen filmin sloganını girin.")
    tagline = await bot.wait_for('message', check=check)
    data.append(tagline.content)

    data.append(7111) #directors.name = NULL
    data.pop(0)
    manager.insert_movie(data)
    await ctx.send("Film kaydedildi")

@bot.command()
async def new_director(director):
    manager.execute("INSERT OR IGNORE INTO directors (name) VALUES(?)", director)

@bot.command()
async def movies(ctx,limit):
    r = manager.execute(f"SELECT title, release_date FROM movies ORDER BY release_date DESC LIMIT {limit}")
    for i in range(r):
        await ctx.send(f"i[0] | i[1]")

@bot.command()
async def director(ctx, diirector):
    r = manager.execute(f"""
SELECT directors.name AS director_name,
    COUNT(*) AS movies_filmed
FROM directors
JOIN movies ON directors.id = movies.director_id
GROUP BY directors.name
HAVING directors.name = {diirector}
ORDER BY movies_filmed DESC;
""")
    await ctx.send(r)

@bot.command()
async def sql_select(ctx, *query: str):
    if query[0] == "SELECT":
        try:
            r = manager.execute(query)
            await ctx.send(r)
        except:
            await ctx.send("Sorgunuz hata verdi veya çıktı vermedi.")

bot.run(TOKEN)