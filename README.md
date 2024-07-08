<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eva Maria Bot</title>
</head>

<body>
    <div style="text-align: center;">
        <img src="assets/logo.jpg" alt="Eva Maria Logo">
        <h1><b>Eva Maria Bot</b></h1>
    </div>

    <div>
        <a href="https://github.com/AM-ROBOTS/EvaMaria/stargazers">
            <img src="https://img.shields.io/github/stars/AM-ROBOTS/EvaMaria?style=flat-square&color=yellow"
                alt="Stars">
        </a>
        <a href="https://github.com/AM-ROBOTS/EvaMaria/fork">
            <img src="https://img.shields.io/github/forks/AM-ROBOTS/EvaMaria?style=flat-square&color=orange"
                alt="Forks">
        </a>
        <a href="https://github.com/AM-ROBOTS/EvaMaria/">
            <img src="https://img.shields.io/github/repo-size/AM-ROBOTS/EvaMaria?style=flat-square&color=green"
                alt="Repo Size">
        </a>
        <a href="https://github.com/AM-ROBOTS/EvaMaria">
            <img src="https://badges.frapsoft.com/os/v2/open-source.svg?v=103" alt="Open Source Love">
        </a>
        <a href="https://github.com/AM-ROBOTS/EvaMaria/graphs/contributors">
            <img src="https://img.shields.io/github/contributors/AM-ROBOTS/EvaMaria?style=flat-square&color=green"
                alt="Contributors">
        </a>
        <a href="https://github.com/AM-ROBOTS/EvaMaria/blob/main/LICENSE">
            <img src="https://img.shields.io/badge/License-AGPL-blue" alt="License">
        </a>
        <a href="https://stars.medv.io/AM-ROBOTS/EvaMaria">
            <img src="https://stars.medv.io/8769ANURAG/EvaMaria.svg" alt="Sparkline">
        </a>
    </div>

    <h2>Features</h2>
    <ul>
        <li>Auto Filter</li>
        <li>Manual Filter</li>
        <li>IMDB</li>
        <li>Admin Commands</li>
        <li>Broadcast</li>
        <li>Index</li>
        <li>IMDB search</li>
        <li>Inline Search</li>
        <li>Random pics</li>
        <li>ids and User info</li>
        <li>Stats, Users, Chats, Ban, Unban, Leave, Disable, Channel</li>
        <li>Spelling Check Feature</li>
        <li>File Store</li>
    </ul>

    <h2>Variables</h2>
    <p>Read <a href="https://telegram.dog/Sources_cods">this</a> before you start messing up with your edits.</p>

    <h3>Required Variables</h3>
    <ul>
        <li><code>BOT_TOKEN</code>: Create a bot using <a href="https://telegram.dog/BotFather">@BotFather</a>, and get the Telegram API token.</li>
        <li><code>API_ID</code>: Get this value from <a href="https://my.telegram.org/apps">telegram.org</a></li>
        <li><code>API_HASH</code>: Get this value from <a href="https://my.telegram.org/apps">telegram.org</a></li>
        <li><code>CHANNELS</code>: Username or ID of channel or group. Separate multiple IDs by space.</li>
        <li><code>ADMINS</code>: Username or ID of Admin. Separate multiple Admins by space.</li>
        <li><code>DATABASE_URI</code>: <a href="https://www.mongodb.com">mongoDB</a> URI. Get this value from <a href="https://www.mongodb.com">mongoDB</a>.</li>
        <li><code>DATABASE_NAME</code>: Name of the database in <a href="https://www.mongodb.com">mongoDB</a>.</li>
        <li><code>LOG_CHANNEL</code>: A channel to log the activities of bot. Make sure bot is an admin in the channel.</li>
    </ul>

    <h3>Optional Variables</h3>
    <ul>
        <li><code>PICS</code>: Telegraph links of images to show in start message. (Multiple images can be used separated by space.)</li>
        <li><code>FILE_STORE_CHANNEL</code>: Channel from where file store links of posts should be made. Separate multiple IDs by space.</li>
    </ul>

    <p>Check <a href="https://github.com/8769ANURAG/EvaMaria/blob/master/info.py">info.py</a> for more details.</p>

    <h2>Deploy</h2>
    <p>You can deploy this bot anywhere:</p>

    <a href="https://dashboard.scalingo.com/create/app?source=https://github.com/AM-ROBOTS/EvaMaria">
        <img src="https://cdn.scalingo.com/deploy/button.svg" alt="Deploy">
    </a>

    <p><i><a href="https://youtu.be/Miajl2amrKo">Watch Deploying Tutorial...</a></i></p>

    <details>
        <summary>Deploy To Heroku</summary>
        <p><br><a href="https://telegram.dog/XTZ_HerokuBot?start=QU0tUk9CT1RTL0V2YU1hcmlhIG1haW4"><img
                    src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy"></a></p>
    </details>

    <details>
        <summary>Deploy To VPS</summary>
        <p><pre>git clone https://github.com/AM-ROBOTS/EvaMaria<br># Install Packages<br>pip3 install -U -r requirements.txt<br>Edit info.py with variables as given below then run bot<br>python3 bot.py</pre></p>
    </details>

    <h2>Commands</h2>
    <pre>
• /logs - to get the recent errors
• /stats - to get status of files in db.
* /filter - add manual filters
* /filters - view filters
* /connect - connect to PM.
* /disconnect - disconnect from PM
* /del - delete a filter
* /delall - delete all filters
* /deleteall - delete all index(autofilter)
* /delete - delete a specific file from index.
* /info - get user info
* /id - get tg ids.
* /imdb - fetch info from imdb.
• /users - to get list of my users and ids.
• /chats - to get list of the my chats and ids 
• /index  - to add files from a channel
• /leave  - to leave from a chat.
• /disable  -  do disable a chat.
* /enable - re-enable chat.
• /ban  - to ban a user.
• /unban  - to unban a user.
• /channel - to get list of total connected channels
• /broadcast - to broadcast a message to all Eva Maria users
• /batch - to create link for multiple posts
• /link - to create link for one post
</pre>

    <h2>Support</h2>
    <a href="https://telegram.dog/Technical_Help_Support_Bot">
        <img src="https://img.shields.io/badge/Telegram-Group-30302f?style=flat&logo=telegram" alt="Telegram Group">
    </a>
    <a href="https://telegram.dog/sources_cods">
        <img src="https://img.shields.io/badge/Telegram-Channel-30302f?style=flat&logo=telegram" alt="Telegram Channel">
    </a>

    <h2>Credits</h2>
    <p><a href="https://telegram.dog/AM_ROBOTS"><img
                src="https://img.shields.io/static/v1?label=EvaMaria&message=devs&color=critical" alt="EvaMaria-Devs"></a></p>

    <h2>Thanks to</h2>
    <ul>
        <li>Thanks To Dan For His Awesome <a href="https://github.com/pyrogram/pyrogram">Library</a></li>
        <li>Thanks To Mahesh For His Ritesh <a href="https://github.com/ritheshrkrm">Evamaria</a></li>
        <li>Thanks To <a href="https://github.com/trojanzhex">Trojanz</a> for Their Awesome <a
                href="https://github.com/TroJanzHEX/Unlimited-Filter-Bot">Unlimited Filter Bot</a> And <a
                href="https://github.com/trojanzhex/auto-filter-bot">AutoFilterBoT</a></li>
        <li>Thanks To All Everyone In This Journey</li>
    </ul>

    <h3>Note</h3>
    <p><a href="https://telegram.dog/subin_works/203">Note To A So Called Dev</a>: Kanging this codes and and editing a few lines and releasing a V.x or an <a
            href="https://telegram.dog/subin_works/204">alpha</a>, beta , gamma branches of your repo won't make you a Developer. Fork the repo and edit as per your needs.</p>

    <h3>Disclaimer</h3>
    <p><a href="https://www.gnu.org/licenses/agpl-3.0.en.html#header"><img
                src="https://www.gnu.org/graphics/agplv3-155x51.png" alt="GNU Affero General Public License 2.0"></a><br>
        Licensed under <a href="https://github.com/EvamariaTG/evamaria/blob/master/LICENSE">GNU AGPL 2.0.</a><br>
        Selling The Codes To Other People For Money Is <b>Strictly Prohibited</b>.</p>

    <h3>Inspiration</h3>
    <p>This is an attempt to create a clone of a BOAT made out of <a
            href="https://telegram.dog/GetTGLink/4187">banana trees 🌳</a></p>

    <a href="https://telegra.ph/file/98342dc186fd7484cba91.mp4">
        <img src="https://telegra.ph/file/e743b0c8a04252774bac2.jpg" alt="For Vaza">
    </a>
</body>

</html>
