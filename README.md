# SteamBud 0.0.1
SteamBud Bot is a simple Discord bot designed to facilitate the search for video game deals using the powerful CheapSharkAPI.

# Features
- `Versatile Deal Lookup` Search for deals using Steam links, Steam app IDs, and game IDs from the CheapShark database, and select your preferred store.
- `Trusted Website Verification` Easily check trusted websites for game deals.
- `Efficient Deal Filtering` Seamlessly filter and refine deal searches to pinpoint the best discounts.

# Commands
- `!sbcmds` - Display the list of available commands.

    ![image](https://github.com/neil-py/SteamBud-Bot/assets/92870064/4942ce70-6354-4aa6-b39d-ad0bc0e9e18a)
- `!stores` - View the list of trusted websites and their respective storeID

    ![image](https://github.com/neil-py/SteamBud-Bot/assets/92870064/687e3596-f529-4501-9609-12ddcf27b765)

- `!searchgame "starfield" 5` - Conduct a general search for game titles, retrieving their respective game IDs, and the cheapest deal information based on the specified amount.

    ![image](https://github.com/neil-py/SteamBud-Bot/assets/92870064/fcb92c11-80e0-44bd-9886-cdfc18416172)
- `!dealsLookUp 1 0 10` - Retrieve the top 10 deals from the selected store within the specified price range.

    ![image](https://github.com/neil-py/SteamBud-Bot/assets/92870064/c3f3e587-e4a4-427e-9e8b-89fc70045e95)

- `!findDeals` - Find deals based on the provided app ID.

    ![image](https://github.com/neil-py/SteamBud-Bot/assets/92870064/307e5442-eaf3-466c-b290-a88c152cff77)

- `!steamID 1716740` - Discover the cheapest deal for a given Steam app ID.

    ![image](https://github.com/neil-py/SteamBud-Bot/assets/92870064/8069aeb7-a5e1-4a37-ae19-64078a151ea8)

- `!steamLINK https://store.steampowered.com/app/1174180/Red_Dead_Redemption_2/` - Find the best deal based on a provided Steam link.

    ![image](https://github.com/neil-py/SteamBud-Bot/assets/92870064/a604212f-1264-49d5-b942-4c97febd7cf0)


# Setup

## Install project modules

```cmd
  pip install -r requirements.txt

```

## Environment Variables
To run this project, ensure you have the following environment variables in your `.env` file:

`TOKEN` - Discord Bot Token

## Configure Discord Bot
- Obtain a token string for your bot by registering your bot at `https://discordapp.com/developers`
- Generate an invitation link following this format `https://discordapp.com/api/oauth2/authorize?client_id={ APPLICATION ID }&permissions=2159044672&scope=bot`
- After creating `.env` paste the discord token

    ```txt
  TOKEN: YOUR_DISCORD_BOT_TOKEN

    ```
## Running the Application
Execute the `bot.py` script to start the bot.

## Acknowledgements

 - [CheapSharkAPI](https://apidocs.cheapshark.com/)


