# Introduction

Ready to get your Python on and create a Discord bot? This guide's got you covered with installation options and a basic bot code example.

### Requirements

- [x] Python 3.10 or greater
- [x] Know how to use `pip`
- [x] [A bot account](02 Creating Your Bot.md)
- [ ] An aversion to puns

## Installing and Setting up a Bot

### Virtual Environments

We strongly recommend that you make use of Virtual Environments when working on any project.
This means that each project will have its own libraries of any version and does not affect anything else on your system.
Don't worry, this isn't setting up a full-fledged virtual machine, just small python environment.

=== ":material-linux: Linux"
    ```shell
    cd "[your bots directory]"
    python3 -m venv venv
    source venv/bin/activate
    ```

=== ":material-microsoft-windows: Windows"
    ```shell
    cd "[your bots directory]"
    py -3 -m venv venv
    venv/Scripts/activate
    ```

It's that simple, now you're using a virtual environment. If you want to leave the environment just type `deactivate`.
If you want to learn more about the virtual environments, check out [this page](https://docs.python.org/3/tutorial/venv.html)

### Pip install

Now let's get the library installed.

=== ":material-linux: Linux"
    ```shell
    python3 -m pip install discord-py-interactions --upgrade
    ```

=== ":material-microsoft-windows: Windows"
    ```shell
    py -3 -m pip install discord-py-interactions --upgrade
    ```

### Basic bot

!!! note
    This is a very basic bot. For a more detailed example/template bot that demonstrates many parts of interactions.py, see [the boilerplate repository.](https://github.com/interactions-py/boilerplate)

Now let's get a basic bot going, for your code, you'll want something like this:

```python
from interactions import Client, Intents, listen

bot = Client(intents=Intents.DEFAULT)
# intents are what events we want to receive from discord, `DEFAULT` is usually fine

@listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


@listen()
async def on_message_create(event):
    # This event is called when a message is sent in a channel the bot can see
    print(f"message received: {event.message.content}")


bot.start("Put your token here")
```

Congratulations! You now have a basic understanding of this library.
If you have any questions check out our other guides, or join the
--8<-- "discord_inv.md"

For more examples, check out the [examples page](/interactions.py/Guides/90 Example)


# Creating Your Bot

To make a bot on Discord, you must first create an application on Discord. Thankfully, Discord has made this process very simple:

1. Login to the [:fontawesome-brands-discord:Discord website](https://discord.com/)

2. Navigate to the [Developer Application page](https://discord.com/developers/applications)

3. Press `New Application`
   <br>![New Application Button](../images/CreatingYourBot/NewApplication.png "The New Application Button")

4. Give your application a name, and press `Create`
    <br>![Create Application Dialogue](../images/CreatingYourBot/CreateAnApplication.png "The Create Application Dialogue")

    ???+ note
        Don't worry if there isn't a `team` option, this only appears if you have a developer team.
        If you have a team and want to assign your bot to it, use this.

5. In the `Bot` tab, press `Add bot`
    <br>![img.png](../images/CreatingYourBot/BuildABot.png "The Add bot button and text")

6. You now have a bot! You're going to want to press `Reset Token` to get your bot's token, so you can start coding
    <br>![A section that shows your bot and its token](../images/CreatingYourBot/BotUserToken.png "The bot display")

    ???+ note
        You may (or may not) be asked to enter your password or 2FA authentication code to confirm this action.

    !!! warning "Warning: Do not share your token!"
        Think of this token as your bots username **and** password in one. You should **never** share this with someone else.
        If someone has your token, they can do absolutely anything with your bot, from banning every member in every server to
        leaving every server your bot is in.

        If you think you have leaked your token, press `Reset Token` on the same page you copy your token on,
        this will revoke your token (logging out all exisitng sessions), and generate a new token for you.

        :fontawesome-brands-github:Github will automatically revoke your token if you accidentally commit it, but don't rely on this
        as a crutch, keep your token safe.


## Inviting your bot!

So you've created a bot, but it's not in a server yet. Lets fix that.

1. On the [Developer Application page](https://discord.com/developers/applications) from above, select your bot

2. Navigate to the `OAuth2` tab

3. Scroll down to the `URL Generator`. This is where we're going to create our invite link
    <br>![A widget that creates your invite link](../images/CreatingYourBot/oauth2Gen.png "The invite oauth2 generator")

4. Select the `bot` option, and if you want to use application commands, select `applications.commands` as well

5. If your bot needs any special permissions, select those below
    <br>![A widget that lets you pick what your bot's permissions are](../images/CreatingYourBot/botPerms.png "Bot Permissions")

6. Now you have an invite link! Simply use this to invite your bot.

    !!! note
        You need `manage server` permissions to add a bot to a server


# Slash Commands

So you want to make a slash command (or interaction, as they are officially called), but don't know how to get started?
Then this is the right place for you.

## Your First Command

To create an interaction, simply define an asynchronous function and use the `@slash_command()` decorator above it.

Interactions need to be responded to within 3 seconds. To do this, use `await ctx.send()`.
If your code needs more time, don't worry. You can use `await ctx.defer()` to increase the time until you need to respond to the command to 15 minutes.
```python
from interactions import slash_command, SlashContext

@slash_command(name="my_command", description="My first command :)")
async def my_command_function(ctx: SlashContext):
    await ctx.send("Hello World")

@slash_command(name="my_long_command", description="My second command :)")
async def my_long_command_function(ctx: SlashContext):
    # need to defer it, otherwise, it fails
    await ctx.defer()

    # do stuff for a bit
    await asyncio.sleep(600)

    await ctx.send("Hello World")
```
???+ note
    Command names must be lowercase and can only contain `-` and `_` as special symbols and must not contain spaces.

When testing, it is recommended to use non-global commands, as they sync instantly.
For that, you can either define `scopes` in every command or set `debug_scope` in the bot instantiation which sets the scope automatically for all commands.

You can define non-global commands by passing a list of guild ids to `scopes` in the interaction creation.
```python
@slash_command(name="my_command", description="My first command :)", scopes=[870046872864165888])
async def my_command_function(ctx: SlashContext):
    await ctx.send("Hello World")
```

For more information, please visit the API reference [here](/interactions.py/API Reference/API Reference/models/Internal/application_commands/#interactions.models.internal.application_commands.slash_command).

## Subcommands

If you have multiple commands that fit under the same category, subcommands are perfect for you.

Let's define a basic subcommand:
```python
@slash_command(
    name="base",
    description="My command base",
    group_name="group",
    group_description="My command group",
    sub_cmd_name="command",
    sub_cmd_description="My command",
)
async def my_command_function(ctx: SlashContext):
    await ctx.send("Hello World")
```

This will show up in discord as `/base group command`. There are more ways to add additional subcommands:

=== ":one: Decorator"
    ```python
    @my_command_function.subcommand(
        group_name="group",
        group_description="My command group",
        sub_cmd_name="sub",
        sub_cmd_description="My subcommand",
    )
    async def my_second_command_function(ctx: SlashContext):
        await ctx.send("Hello World")
    ```

=== ":two: Repeat Definition"
    ```python
    @slash_command(
        name="base",
        description="My command base",
        group_name="group",
        group_description="My command group",
        sub_cmd_name="second_command",
        sub_cmd_description="My second command",
    )
    async def my_second_command_function(ctx: SlashContext):
        await ctx.send("Hello World")
    ```

    **Note:** This is particularly useful if you want to split subcommands into different files.

=== ":three: Class Definition"
    ```python
    from interactions import SlashCommand

    base = SlashCommand(name="base", description="My command base")
    group = base.group(name="group", description="My command group")

    @group.subcommand(sub_cmd_name="second_command", sub_cmd_description="My second command")
    async def my_second_command_function(ctx: SlashContext):
        await ctx.send("Hello World")
    ```

For all of these, the "group" parts are optional, allowing you to do `/base command` instead.

???+ note
    You cannot mix group subcommands and non-group subcommands into one base command - you must either use all group subcommands or normal subcommands.


## Options

Interactions can also have options. There are a bunch of different [types of options](/interactions.py/API Reference/API Reference/models/Internal/application_commands/#interactions.models.internal.application_commands.OptionType):

| Option Type               | Return Type                                | Description                                                                                 |
|---------------------------|--------------------------------------------|---------------------------------------------------------------------------------------------|
| `OptionType.STRING`      | `str`                                      | Limit the input to a string.                                                                |
| `OptionType.INTEGER`     | `int`                                      | Limit the input to a integer.                                                               |
| `OptionType.NUMBER`      | `float`                                    | Limit the input to a float.                                                                 |
| `OptionType.BOOLEAN`     | `bool`                                     | Let the user choose either `True` or `False`.                                               |
| `OptionType.USER`        | `Member` in guilds, else `User`            | Let the user choose a discord user from an automatically-generated list of options.         |
| `OptionType.CHANNEL`     | `GuildChannel` in guilds, else `DMChannel` | Let the user choose a discord channel from an automatically-generated list of options.      |
| `OptionType.ROLE`        | `Role`                                     | Let the user choose a discord role from an automatically-generated list of options.         |
| `OptionType.MENTIONABLE` | `DiscordObject`                            | Let the user chose any discord mentionable from an automatically generated list of options. |
| `OptionType.ATTACHMENT`  | `Attachment`                               | Let the user upload an attachment.                                                          |

Now that you know all the options you have for options, you can opt into adding options to your interaction.

You do that by using the `@slash_option()` decorator and passing the option name as a function parameter:
```python
from interactions import OptionType, slash_option

@slash_command(name="my_command", ...)
@slash_option(
    name="integer_option",
    description="Integer Option",
    required=True,
    opt_type=OptionType.INTEGER
)
async def my_command_function(ctx: SlashContext, integer_option: int):
    await ctx.send(f"You input {integer_option}")
```

Options can either be required or not. If an option is not required, make sure to set a default value for them.

Always make sure to define all required options first, this is a Discord requirement!
```python
@slash_command(name="my_command", ...)
@slash_option(
    name="integer_option",
    description="Integer Option",
    required=False,
    opt_type=OptionType.INTEGER
)
async def my_command_function(ctx: SlashContext, integer_option: int = 5):
    await ctx.send(f"You input {integer_option}")
```

For more information, please visit the API reference [here](/interactions.py/API Reference/API Reference/models/Internal/application_commands/#interactions.models.internal.application_commands.slash_option).

### Restricting Options

If you are using an `OptionType.CHANNEL` option, you can restrict the channel a user can choose by setting `channel_types`:
```python
from interactions import ChannelType, GuildText, OptionType, SlashContext, slash_command, slash_option

@slash_command(name="my_command")
@slash_option(
    name="channel_option",
    description="Channel Option",
    required=True,
    opt_type=OptionType.CHANNEL,
    channel_types=[ChannelType.GUILD_TEXT],
)
async def my_command_function(ctx: SlashContext, channel_option: GuildText):
    await channel_option.send("This is a text channel in a guild")

    await ctx.send("...")
```

You can also set an upper and lower limit for both `OptionType.INTEGER` and `OptionType.NUMBER` by setting `min_value` and `max_value`:
```python
@slash_command(name="my_command", ...)
@slash_option(
    name="integer_option",
    description="Integer Option",
    required=True,
    opt_type=OptionType.INTEGER,
    min_value=10,
    max_value=15
)
async def my_command_function(ctx: SlashContext, integer_option: int):
    await ctx.send(f"You input {integer_option} which is always between 10 and 15")
```

The same can be done with the length of an option when using `OptionType.STRING` by setting `min_length` and `max_length`:
```python
@slash_command(name="my_command", ...)
@slash_option(
    name="string_option",
    description="String Option",
    required=True,
    opt_type=OptionType.STRING,
    min_length=5,
    max_length=10
)
async def my_command_function(ctx: SlashContext, string_option: str):
    await ctx.send(f"You input `{string_option}` which is between 5 and 10 characters long")
```

!!! danger "Option Names"
    Be aware that the option `name` and the function parameter need to be the same (In this example both are `integer_option`).


## Option Choices

If your users ~~are dumb~~ constantly misspell specific strings, it might be wise to set up choices.
With choices, the user can no longer freely input whatever they want, instead, they must choose from a pre-defined list.

To create a choice, simply fill `choices` in `@slash_option()`. An option can have up to 25 choices. The name of a choice is what will be shown in the Discord client of the user, while the value is what the bot will receive in its callback. Both can be the same.
```python
from interactions import SlashCommandChoice

@slash_command(name="my_command", ...)
@slash_option(
    name="integer_option",
    description="Integer Option",
    required=True,
    opt_type=OptionType.INTEGER,
    choices=[
        SlashCommandChoice(name="One", value=1),
        SlashCommandChoice(name="Two", value=2)
    ]
)
async def my_command_function(ctx: SlashContext, integer_option: int):
    await ctx.send(f"You input {integer_option} which is either 1 or 2")
```

For more information, please visit the API reference [here](/interactions.py/API Reference/API Reference/models/Internal/application_commands/#interactions.models.internal.application_commands.SlashCommandChoice).

## Autocomplete / More than 25 choices needed

If you have more than 25 choices the user can choose from, or you want to give a dynamic list of choices depending on what the user is currently typing, then you will need autocomplete options.
The downside is that you need to supply the choices on request, making this a bit more tricky to set up.

To use autocomplete options, set `autocomplete=True` in `@slash_option()`:
```python
@slash_command(name="my_command", ...)
@slash_option(
    name="string_option",
    description="String Option",
    required=True,
    opt_type=OptionType.STRING,
    autocomplete=True
)
async def my_command_function(ctx: SlashContext, string_option: str):
    await ctx.send(f"You input {string_option}")
```

Then you need to register the autocomplete callback, aka the function Discord calls when users fill in the option.

In there, you have three seconds to return whatever choices you want to the user. In this example we will simply return their input with "a", "b" or "c" appended:
```python
from interactions import AutocompleteContext

@my_command_function.autocomplete("string_option")
async def autocomplete(self, ctx: AutocompleteContext):
    string_option_input = ctx.input_text  # can be empty
    # you can use ctx.kwargs.get("name") to get the current state of other options - note they can be empty too

    # make sure you respond within three seconds
    await ctx.send(
        choices=[
            {
                "name": f"{string_option_input}a",
                "value": f"{string_option_input}a",
            },
            {
                "name": f"{string_option_input}b",
                "value": f"{string_option_input}b",
            },
            {
                "name": f"{string_option_input}c",
                "value": f"{string_option_input}c",
            },
        ]
    )
```

## Command definition without decorators

There are currently four different ways to define interactions, one does not need any decorators at all.

=== ":one: Multiple Decorators"

    ```python
    @slash_command(name="my_command", description="My first command :)")
    @slash_option(
        name="integer_option",
        description="Integer Option",
        required=True,
        opt_type=OptionType.INTEGER
    )
    async def my_command_function(ctx: SlashContext, integer_option: int):
        await ctx.send(f"You input {integer_option}")
    ```

=== ":two: Single Decorator"

    ```python
    from interactions import SlashCommandOption

    @slash_command(
        name="my_command",
        description="My first command :)",
        options=[
            SlashCommandOption(
                name="integer_option",
                description="Integer Option",
                required=True,
                type=OptionType.INTEGER
            )
        ]
    )
    async def my_command_function(ctx: SlashContext, integer_option: int):
        await ctx.send(f"You input {integer_option}")
    ```

=== ":three: Function Annotations"

    ```python
    from interactions import slash_int_option

    @slash_command(name="my_command", description="My first command :)")
    async def my_command_function(ctx: SlashContext, integer_option: slash_int_option("Integer Option")):
        await ctx.send(f"You input {integer_option}")
    ```

=== ":four: Manual Registration"

    ```python
    from interactions import SlashCommandOption

    async def my_command_function(ctx: SlashContext, integer_option: int):
        await ctx.send(f"You input {integer_option}")

    bot.add_interaction(
        command=SlashCommand(
            name="my_command",
            description="My first command :)",
            options=[
                SlashCommandOption(
                    name="integer_option",
                    description="Integer Option",
                    required=True,
                    type=OptionType.INTEGER
                )
            ]
        )
    )
    ```

## Restrict commands using permissions

It is possible to disable interactions (slash commands as well as context menus) for users that do not have a set of permissions.

This functionality works for **permissions**, not to confuse with roles. If you want to restrict some command if the user does not have a certain role, this cannot be done on the bot side. However, it can be done on the Discord server side, in the Server Settings > Integrations page.

!!!warning Administrators
    Remember that administrators of a Discord server have all permissions and therefore will always see the commands.

    If you do not want admins to be able to overwrite your permissions, or the permissions are not flexible enough for you, you should use [checks][checks].

In this example, we will limit access to the command to members with the `MANAGE_EVENTS` and `MANAGE_THREADS` permissions.
There are two ways to define permissions.

=== ":one: Decorators"

    ```python
    from interactions import Permissions, slash_default_member_permission

    @slash_command(name="my_command")
    @slash_default_member_permission(Permissions.MANAGE_EVENTS | Permissions.MANAGE_THREADS)
    async def my_command_function(ctx: SlashContext):
        ...
    ```

=== ":two: Function Definition"

    ```python
    from interactions import Permissions

    @slash_command(
        name="my_command",
        default_member_permissions=Permissions.MANAGE_EVENTS | Permissions.MANAGE_THREADS,
    )
    async def my_command_function(ctx: SlashContext):
        ...
    ```

Multiple permissions are defined with the bitwise OR operator `|`.

### Blocking Commands in DMs

You can also block commands in DMs. To do that, just set `dm_permission` to false.

```py
@slash_command(
    name="my_guild_only_command",
    dm_permission=False,
)
async def my_command_function(ctx: SlashContext):
    ...
```

## Checks

Checks allow you to define who can use your commands however you want.

There are a few pre-made checks for you to use, and you can simply create your own custom checks.

=== ":one: Built-In Check"
    Check that the author is the owner of the bot:

    ```python
    from interactions import SlashContext, check, is_owner, slash_command

    @slash_command(name="my_command")
    @check(is_owner())
    async def command(ctx: SlashContext):
        await ctx.send("You are the owner of the bot!", ephemeral=True)
    ```

=== ":two: Custom Check"
    Check that the author's username starts with `a`:

    ```python
    from interactions import BaseContext, SlashContext, check, slash_command

    async def my_check(ctx: BaseContext):
        return ctx.author.username.startswith("a")

    @slash_command(name="my_command")
    @check(my_check)
    async def command(ctx: SlashContext):
        await ctx.send("Your username starts with an 'a'!", ephemeral=True)
    ```

=== ":three: Reusing Checks"
    You can reuse checks in extensions by adding them to the extension check list

    ```python
    from interactions import Extension

    class MyExtension(Extension):
        def __init__(self, bot) -> None:
            super().__init__(bot)
            self.add_ext_check(is_owner())

    @slash_command(name="my_command")
    async def my_command_function(ctx: SlashContext):
        ...

    @slash_command(name="my_command2")
    async def my_command_function2(ctx: SlashContext):
        ...
    ```

    The check will be checked for every command in the extension.


## Avoid redefining the same option everytime

If you have multiple commands that all use the same option, it might be both annoying and bad programming to redefine it multiple times.

Luckily, you can simply make your own decorators that themselves call `@slash_option()`:
```python
def my_own_int_option():
    """Call with `@my_own_int_option()`"""

    def wrapper(func):
        return slash_option(
            name="integer_option",
            description="Integer Option",
            opt_type=OptionType.INTEGER,
            required=True
        )(func)

    return wrapper


@slash_command(name="my_command", ...)
@my_own_int_option()
async def my_command_function(ctx: SlashContext, integer_option: int):
    await ctx.send(f"You input {integer_option}")
```

The same principle can be used to reuse autocomplete options.

## Simplified Error Handling

If you want error handling for all commands, you can override the default error listener and define your own.
Any error from interactions will trigger `CommandError`. That includes context menus.

In this example, we are logging the error and responding to the interaction if not done so yet:
```python
import traceback
from interactions.api.events import CommandError

@listen(CommandError, disable_default_listeners=True)  # tell the dispatcher that this replaces the default listener
async def on_command_error(self, event: CommandError):
    traceback.print_exception(event.error)
    if not event.ctx.responded:
        await event.ctx.send("Something went wrong.")
```

There also is `CommandCompletion` which you can overwrite too. That fires on every interactions usage.

## Custom Parameter Type

If your bot is complex enough, you might find yourself wanting to use custom models in your commands.

To do this, you'll want to use a string option, and define a converter. Information on how to use converters can be found [on the converter page](../08 Converters).

## Prefixed/Text Commands

To use prefixed commands, instead of typing `/my_command`, you will need to type instead `!my_command`, provided that the prefix you set is `!`.

Hybrid commands are are slash commands that also get converted to an equivalent prefixed command under the hood. They are their own extension, and require [prefixed commands to be set up beforehand](/interactions.py/Guides/26 Prefixed Commands). After that, use the `setup` function in the `hybrid_commands` extension in your main bot file.

Your setup can (but doesn't necessarily have to) look like this:

```python
import interactions
from interactions.ext import prefixed_commands as prefixed
from interactions.ext import hybrid_commands as hybrid

bot = interactions.Client(...)  # may want to enable the message content intent
prefixed.setup(bot)  # normal step for prefixed commands
hybrid.setup(bot)  # note its usage AFTER prefixed commands have been set up
```

To actually make slash commands, simply replace `@slash_command` with `@hybrid_slash_command`, and `SlashContext` with `HybridContext`, like so:

```python
from interactions.ext.hybrid_commands import hybrid_slash_command, HybridContext

@hybrid_slash_command(name="my_command", description="My hybrid command!")
async def my_command_function(ctx: HybridContext):
    await ctx.send("Hello World")
```

Suggesting you are using the default mention settings for your bot, you should be able to run this command by `@BotPing my_command`.

As you can see, the only difference between hybrid commands and slash commands, from a developer perspective, is that they use `HybridContext`, which attempts
to seamlessly allow using the same context for slash and prefixed commands. You can always get the underlying context via `inner_context`, though.

Of course, keep in mind that supporting two different types of commands is hard - some features may not get represented well in prefixed commands, and autocomplete is not possible at all.


# Context Menus

Context menus are interactions under the hood. Defining them is very similar.
Context menus work off `ctx.target` which contains the object the user interacted with.

You can also define `scopes` and `permissions` for them, just like with interactions.

For more information, please visit the API reference [here](/interactions.py/API Reference/API Reference/models/Internal/application_commands/#interactions.models.internal.application_commands.context_menu).

## Message Context Menus

These open up if you right-click a message and choose `Apps`.

This example repeats the selected message:

```python
from interactions import ContextMenuContext, Message, message_context_menu

@message_context_menu(name="repeat")
async def repeat(ctx: ContextMenuContext):
    message: Message = ctx.target
    await ctx.send(message.content)
```

## User Context Menus

These open up if you right-click a user and choose `Apps`.

This example pings the user:

```python
from interactions import user_context_menu, Member

@user_context_menu(name="ping")
async def ping(ctx: ContextMenuContext):
    member: Member = ctx.target
    await ctx.send(member.mention)
```
???+ note
    Unlike Slash command names, context menu command names **can** be uppercase, contain special symbols and spaces.


# Components

Components (Buttons, Select Menus and soon Text Input Fields) can be added to any message by passing them to the `components` argument in any `.send()` method.

## Layout

All types of components must be part of Action Rows, which are containers that a message can have. Each message can have up to 5 action rows, with each action row containing a maximum of 5 buttons OR a single select menu.

If you don't really care of the layout in which your components are set, you can pass in directly the components without actually creating the Action Rows - the library will handle it itself. However, if the layout is important for you (let's say, you want a row with 3 buttons, then a row with a select menu and finally another row with 2 buttons), then you will need to specify the layout yourself by either defining the action rows or using the `spread_to_rows()` function.

They are organised in a 5x5 grid, so you either have to manage the layout yourself, use `spread_to_rows()` where we organise them for you, or have a single component.

If you want to define the layout yourself, you have to put them in an `ActionRow()`. The `components` parameter need a list of up to five `ActionRow()`.

=== ":one: No special layout"
    Your list of components will be transformed into `ActionRow`s behind the scenes.

    ```python
    from interactions import Button, ButtonStyle

    components = Button(
        style=ButtonStyle.GREEN,
        label="Click Me",
    )

    await channel.send("Look, Buttons!", components=components)
    ```

=== ":two: `ActionRow()`"
    ```python
    from interactions import ActionRow, Button, ButtonStyle

    components: list[ActionRow] = [
        ActionRow(
            Button(
                style=ButtonStyle.GREEN,
                label="Click Me",
            ),
            Button(
                style=ButtonStyle.GREEN,
                label="Click Me Too",
            )
        )
    ]

    await channel.send("Look, Buttons!", components=components)
    ```

=== ":three: `spread_to_rows()`"
    ```python
    from interactions import ActionRow, Button, ButtonStyle, spread_to_rows

    components: list[ActionRow] = spread_to_rows(
        Button(
            style=ButtonStyle.GREEN,
            label="Click Me",
        ),
        Button(
            style=ButtonStyle.GREEN,
            label="Click Me Too",
        )
    )

    await channel.send("Look, Buttons!", components=components)
    ```

For simplicity's sake, example one will be used for all examples going forward.

If you want to delete components, you need to pass `components=[]` to `.edit()`.

## Buttons

Buttons can be clicked on, or be set as disabled if you wish.

```python
components = Button(
    style=ButtonStyle.GREEN,
    label="Click Me",
    disabled=False,
)

await channel.send("Look a Button!", components=components)
```

For more information, please visit the API reference [here](/interactions.py/API Reference/API Reference/models/Discord/components/#interactions.models.discord.components.Button).

### Button Styles

There are a bunch of colours and styles you can choose from.
    <br>![Button Colours](../images/Components/buttons.png "Button Colours")

The colours correspond to the styles found in `ButtonStyle`. Click [here](/interactions.py/API Reference/API Reference/models/Discord/enums/#interactions.models.discord.enums.ButtonStyle) for more information.

If you use `ButtonStyle.URL`, you can pass a URL to the button with the `url` argument. Users who click the button will get redirected to your URL.
```python
from interactions import ButtonStyle

components = Button(
    style=ButtonStyle.URL,
    label="Click Me",
    url="https://github.com/interactions-py/interactions.py",
)

await channel.send("Look a Button!", components=components)
```

`ButtonStyle.URL` does not receive events, or work with callbacks.

## Select Menus

Sometimes there might be more than a handful options which users need to decide between. That's when a `SelectMenu` should probably be used.

Select Menus are very similar to Buttons. The main difference is that you get a list of options to choose from.

If you want to use string options, then you use the `StringSelectMenu`. Simply pass a list of strings to `options` and you are good to go. You can also explicitly pass `SelectOptions` to control the value attribute.

You can also define how many options users can choose by setting `min_values` and `max_values`.

```python
from interactions import StringSelectMenu

components = StringSelectMenu(
    "Pizza", "Pasta", "Burger", "Salad",
    placeholder="What is your favourite food?",
    min_values=1,
    max_values=1,
)

await channel.send("Look a Select!", components=components)
```
???+ note
    You can only have up to 25 options in a Select

Alternatively, you can use `RoleSelectMenu`, `UserSelectMenu` and `ChannelSelectMenu` to select roles, users and channels respectively. These select menus are very similar to `StringSelectMenu`, but they don't allow you to pass a list of options; it's all done behind the scenes.

For more information, please visit the API reference [here](/interactions.py/API Reference/API Reference/models/Discord/components/#interactions.models.discord.components.Select).

## Responding

Now that we know how to send components, we need to learn how to respond to a user when a component is interacted with.
There are three ways to respond to components.

If you add your component to a temporary message asking for additional user input, you should probably use `bot.wait_for_component()`.
These have the downside that, for example, they won't work anymore after restarting your bot. On the positive side, they are defined in the same function where your button is sent, so you can easily use variables that you defined *before* the user used the component.

Otherwise, you are looking for a persistent callback. For that, you want to define a `custom_id` when creating your component.

When responding to a component you need to satisfy Discord either by responding to the context with `ctx.send()` or by editing the component with `ctx.edit_origin()`.

=== ":one: `bot.wait_for_component()`"
    This function supports checks and timeouts.

    In this example, we are checking that the username starts with "a" and clicks the button within 30 seconds. If his username doesn't start with an "a", then we send it an ephemeral message to notify him. If the button times out, we edit the message so that the button is disabled and cannot be clicked anymore.

    ```python
    from interactions import Button, ButtonStyle
    from interactions.api.events import Component

    # defining and sending the button
    button = Button(
        custom_id="my_button_id",
        style=ButtonStyle.GREEN,
        label="Click Me",
    )
    message = await channel.send("Look a Button!", components=button)

    # define the check
    async def check(component: Component) -> bool:
        if component.ctx.author.username.startswith("a"):
            return True
        else:
            await component.ctx.send("Your name does not start with an 'a'!", ephemeral=True)

    try:
        # you need to pass the component you want to listen for here
        # you can also pass an ActionRow, or a list of ActionRows. Then a press on any component in there will be listened for
        used_component: Component = await bot.wait_for_component(components=button, check=check, timeout=30)

    except TimeoutError:
        print("Timed Out!")

        button.disabled = True
        await message.edit(components=button)

    else:
        await used_component.ctx.send("Your name starts with 'a'")
    ```

    You can also use this to check for a normal message instead of a component interaction.

    For more information, please visit the API reference [here](/interactions.py/API Reference/API Reference/client/#interactions.client.client.Client.wait_for_component).


=== ":two: Persistent Callback: `@listen()`"
    You can listen to the `on_component()` event and then handle your callback. This works even after restarts!

    ```python
    from interactions import Button, ButtonStyle
    from interactions.api.events import Component

    # defining and sending the button
    button = Button(
        custom_id="my_button_id",
        style=ButtonStyle.GREEN,
        label="Click Me",
    )
    await channel.send("Look a Button!", components=button)

    @listen(Component)
    async def on_component(event: Component):
        ctx = event.ctx

        match ctx.custom_id:
            case "my_button_id":
                await ctx.send("You clicked it!")
    ```

=== ":three: Persistent Callback: `@component_callback()`"
    If you have a lot of components, putting everything in the `on_component()` event can get messy really quick.

    Similarly to Option 1, you can define `@component_callback` listeners. This works after restarts too.

    You have to pass your `custom_id` to `@component_callback(custom_id)` for the library to be able to register the callback function to the wanted component.

    ```python
    from interactions import Button, ButtonStyle, ComponentContext, component_callback

    # defining and sending the button
    button = Button(
        custom_id="my_button_id",
        style=ButtonStyle.GREEN,
        label="Click Me",
    )
    await channel.send("Look a Button!", components=button)

    # you need to pass your custom_id to this decorator
    @component_callback("my_button_id")
    async def my_callback(ctx: ComponentContext):
        await ctx.send("You clicked it!")
    ```

=== ":four: Persistent Callbacks, with regex"
    Regex (regular expressions) can be a great way to pass information from the component creation directly to the component response callback, in a persistent manner.

    Below is an example of how regex can be used to create a button and how to respond to it.

    ```python
    import re
    from interactions import Button, ButtonStyle, ComponentContext, SlashContext, component_callback, slash_command

    @slash_command(name="test")
    async def command(ctx: SlashContext):
        id = "123456789"  # random ID, could be anything (a member ID, a message ID...)
        button = Button(
            custom_id=f"button_{id}",
            style=ButtonStyle.GREEN,
            label="Click Me",
        )
        await ctx.send(components=button)


    # define the pattern of the button custom_id
    regex_pattern = re.compile(r"button_([0-9]+)")

    @component_callback(regex_pattern)
    async def button_callback(ctx: ComponentContext):
        match = regex_pattern.match(ctx.custom_id)
        if match:
            id = match.group(1)  # extract the ID from the custom ID
            await ctx.send(f"Custom ID: {ctx.custom_id}. ID: {id}")  # will return: "Custom ID: button_123456789. ID: 123456789"
    ```

    Just like normal `@component_callback`, you can specify a regex pattern to match your custom_ids, instead of explicitly passing strings.
    This is useful if you have a lot of components with similar custom_ids, and you want to handle them all in the same callback.

    Please do bare in mind that using regex patterns can be a bit slower than using strings, especially if you have a lot of components.

???+ note
    As explained previously, the main difference between a Button and a Select Menu is that you can retrieve a list of options that were chosen by the user for a Select Menu.
    In this case, this list of options can be found in `ctx.values`.


# Modals

Modals are basically popups which a user can use to send text information to your bot. As of the writing of this guide, you can use two components in a modal:

- Short Text Input (single-line)
- Paragraph Text Input (multi-line)

Each component that you define in your modal must have its own `custom_id` so that you can easily retrieve the data that a user sent later.


## Creating a Modal

Modals are one of the ways you can respond to interactions. They are intended for when you need to query a lot of information from a user.

Modals are valid responses to Slash Commands and Components.
You **cannot** respond to a modal with a modal.
Use `ctx.send_modal()` to send a modal.

```python
from interactions import Modal, ParagraphText, ShortText, SlashContext, slash_command

@slash_command(name="my_modal_command", description="Playing with Modals")
async def my_command_function(ctx: SlashContext):
    my_modal = Modal(
        ShortText(label="Short Input Text", custom_id="short_text"),
        ParagraphText(label="Long Input Text", custom_id="long_text"),
        title="My Modal",
    )
    await ctx.send_modal(modal=my_modal)
```

This example leads to the following modal:
    <br>![example_modal.png](../images/Modals/modal_example.png "The Add bot button and text")

### Text Inputs Customisation

Modal components are customisable in their appearance. You can set a placeholder, pre-fill them, restrict what users can input, or make them optional.

```python
from interactions import Modal, ShortText, SlashContext, slash_command

@slash_command(name="my_modal_command", description="Playing with Modals")
async def my_command_function(ctx: SlashContext):
    my_modal = Modal(
        ShortText(
            label="Short Input Text",
            custom_id="short_text",
            value="Pre-filled text",
            min_length=10,
        ),
        ShortText(
            label="Short Input Text",
            custom_id="optional_short_text",
            required=False,
            placeholder="Please be concise",
            max_length=10,
        ),
        title="My Modal",
    )
    await ctx.send_modal(modal=my_modal)
```

This example leads to the following modal:
    <br>![example_modal.png](../images/Modals/modal_example_customisiblity.png "The Add bot button and text")

## Responding

Now that users have input some information, the bot needs to process it and answer back the user. Similarly to the Components guide, there is a persistent and non-persistent way to listen to a modal answer.

The data that the user has input can be found in `ctx.responses`, which is a dictionary with the keys being the custom IDs of your text inputs and the values being the answers the user has entered.

=== ":one: `@bot.wait_for_modal()`"
    As with `bot.wait_for_component()`, `bot.wait_for_modal()` supports timeouts. However, checks are not supported, since modals are not persistent like Components, and only visible to the interaction invoker.

    ```python
    from interactions import Modal, ModalContext, ParagraphText, ShortText, SlashContext, slash_command

    @slash_command(name="test")
    async def command(ctx: SlashContext):
        my_modal = Modal(
            ShortText(label="Short Input Text", custom_id="short_text"),
            ParagraphText(label="Long Input Text", custom_id="long_text"),
            title="My Modal",
            custom_id="my_modal",
        )
        await ctx.send_modal(modal=my_modal)
        modal_ctx: ModalContext = await ctx.bot.wait_for_modal(my_modal)

        # extract the answers from the responses dictionary
        short_text = modal_ctx.responses["short_text"]
        long_text = modal_ctx.responses["long_text"]

        await modal_ctx.send(f"Short text: {short_text}, Paragraph text: {long_text}", ephemeral=True)
    ```

    !!!warning
        In this example, make sure to not mix the two Contexts `ctx` and `modal_ctx`! If the last line of the code is replaced by `ctx.send()`, the text would not be sent because you have already answered the `ctx` variable previously, when sending the modal (`ctx.send_modal()`).

=== ":two: Persistent Callback: `@modal_callback()`"
    In the case of a persistent callback, your callback function must have the names of the custom IDs of your text inputs as its arguments, similar to how you define a callback for a slash command.

    ```python
    from interactions import Modal, ModalContext, ParagraphText, ShortText, SlashContext, modal_callback, slash_command

    @slash_command(name="test")
    async def command(ctx: SlashContext):
        my_modal = Modal(
            ShortText(label="Short Input Text", custom_id="short_text"),
            ParagraphText(label="Long Input Text", custom_id="long_text"),
            title="My Modal",
            custom_id="my_modal",
        )
        await ctx.send_modal(modal=my_modal)

    @modal_callback("my_modal")
    async def on_modal_answer(ctx: ModalContext, short_text: str, long_text: str):
        await ctx.send(f"Short text: {short_text}, Paragraph text: {long_text}", ephemeral=True)
    ```


# Converters

If your bot is complex enough, you might find yourself wanting to use custom models in your commands. Converters are classes that allow you to do just that, and can be used in both slash and prefixed commands.

This can be useful if you frequently find yourself starting commands with `thing = lookup(thing_name)`.

## Inline Converters

If you do not wish to create an entirely new class, you can simply add a `convert` function in your existing class:

```python
class DatabaseEntry():
    name: str
    description: str
    score: int

    @classmethod  # you can also use staticmethod
    async def convert(cls, ctx: BaseContext, value: str) -> DatabaseEntry:
        """This is where the magic happens"""
        return cls(hypothetical_database.lookup(ctx.guild.id, value))

# Slash Command:
@slash_command(name="lookup", description="Gives info about a thing from the db")
@slash_option(
    name="thing",
    description="The user enters a string",
    required=True,
    opt_type=OptionType.STRING
)
async def my_command_function(ctx: SlashContext, thing: DatabaseEntry):
    await ctx.send(f"***{thing.name}***\n{thing.description}\nScore: {thing.score}/10")

# Prefixed Command:
@prefixed_command()
async def my_command_function(ctx: SlashContext, thing: DatabaseEntry):
    await ctx.reply(f"***{thing.name}***\n{thing.description}\nScore: {thing.score}/10")
```

As you can see, a converter can transparently convert what Discord sends you (a string, a user, etc) into something more complex (a pokemon card, a scoresheet, etc).

## `Converter`

You may also use the `Converter` class that `interactions.py` has as well.

```python
from interactions import Converter

class UpperConverter(Converter):
    async def convert(ctx: BaseContext, argument: str):
        return argument.upper()

# Slash Command:
@slash_command(name="upper", description="Sends back the input in all caps.")
@slash_option(
    name="to_upper",
    description="The thing to make all caps.",
    required=True,
    opt_type=OptionType.STRING
)
async def upper(ctx: SlashContext, to_upper: UpperConverter):
    await ctx.send(to_upper)

# Prefixed Command:
@prefixed_command()
async def upper(ctx: PrefixedContext, to_upper: UpperConverter):
    await ctx.reply(to_upper)
```

## Discord Model Converters

There are `Converter`s that represent some Discord models that you can subclass from. These are largely useful for prefixed commands, but you may find a use for them elsewhere.

A table of objects and their respective converter is as follows:

| Discord Model                          | Converter                     |
|----------------------------------------|-------------------------------|
| `SnowflakeObject`                      | `SnowflakeConverter`          |
| `BaseChannel`, `TYPE_ALL_CHANNEL`      | `BaseChannelConverter`        |
| `DMChannel`, `TYPE_DM_CHANNEL`         | `DMChannelConverter`          |
| `DM`                                   | `DMConverter`                 |
| `DMGroup`                              | `DMGroupConverter`            |
| `GuildChannel`, `TYPE_GUILD_CHANNEL`   | `GuildChannelConverter`       |
| `GuildNews`                            | `GuildNewsConverter`          |
| `GuildCategory`                        | `GuildCategoryConverter`      |
| `GuildText`                            | `GuildTextConverter`          |
| `ThreadChannel`, `TYPE_THREAD_CHANNEL` | `ThreadChannelConverter`      |
| `GuildNewsThread`                      | `GuildNewsThreadConverter`    |
| `GuildPublicThread`                    | `GuildPublicThreadConverter`  |
| `GuildPrivateThread`                   | `GuildPrivateThreadConverter` |
| `VoiceChannel`, `TYPE_VOICE_CHANNEL`   | `VoiceChannelConverter`       |
| `GuildVoice`                           | `GuildVoiceConverter`         |
| `GuildStageVoice`                      | `GuildStageVoiceConverter`    |
| `TYPE_MESSAGEABLE_CHANNEL`             | `MessageableChannelConverter` |
| `User`                                 | `UserConverter`               |
| `Member`                               | `MemberConverter`             |
| `Guild`                                | `GuildConverter`              |
| `Role`                                 | `RoleConverter`               |
| `PartialEmoji`                         | `PartialEmojiConverter`       |
| `CustomEmoji`                          | `CustomEmojiConverter`        |


## `typing.Annotated`

Using `typing.Annotated` can allow you to have more proper typehints when using converters:

```python
from typing import Annotated

class UpperConverter(Converter):
    async def convert(ctx: BaseContext, argument: str):
        return argument.upper()

# Slash Command:
@slash_command(name="upper", description="Sends back the input in all caps.")
@slash_option(
    name="to_upper",
    description="The thing to make all caps.",
    required=True,
    opt_type=OptionType.STRING
)
async def upper(ctx: SlashContext, to_upper: Annotated[str, UpperConverter]):
    await ctx.send(to_upper)

# Prefixed Command:
@prefixed_command()
async def upper(ctx: PrefixedContext, to_upper: Annotated[str, UpperConverter]):
    await ctx.reply(to_upper)
```

For slash commands, `interactions.py` will find the first argument in `Annotated` (besides for the first argument) that are like the converters in this guide and use that.
For prefixed commands, `interactions.py` will always use the second parameter in `Annotated` as the actual converter/parameter to process.


# Events

Events (in interactions.py) are pieces of information that are sent whenever something happens in Discord or in the library itself - this includes channel updates, message sending, the bot starting up, and more.

## Intents

What events you subscribe to are defined at startup by setting your `Intents`.

By default, interactions.py automatically uses every intent but privileged intents (discussed in a bit). This means you're receiving data about *a lot* of events - it's nice to have those intents while starting out, but we heavily encourage narrowing them so that your bot uses less memory and isn't slowed down by processing them.

There are two ways of setting them. We'll use the `GUILDS` and `GUILD_INVITES` intents as an example, but you should decide what intents you need yourself.

=== ":one: Directly through `Intents`"
    ```python
    from interactions import Client, Intents
    bot = Client(intents=Intents.GUILDS | Intents.GUILD_INVITES)
    ```

=== ":two: `Intents.new`"
    ```python
    from interactions import Client, Intents
    bot = Client(intents=Intents.new(guilds=True, guild_invites=True))
    ```

Some intents are deemed to have sensitive content by Discord and so have extra restrictions on them - these are called **privileged intents.** At the time of writing, these include *message content, guild members, and presences.* These require extra steps to enable them for your bot:

1. Go to the [Discord developer portal](https://discord.com/developers/applications/).
2. Select your application.
3. In the "Bot" tab, go to the "Privileged Gateway Intents" category and scroll down to the privileged intents you want.
4. Enable the toggle.
    - **If your bot is verified or in more than 100 servers, you need to apply for the intent through Discord in order to toggle it.** This may take a couple of weeks.

Then, you can specify it in your bot just like the other intents. If you encounter any errors during this process, [referring to the intents page on Discord's documentation](https://discord.com/developers/docs/topics/gateway#gateway-intents) may help.

!!! danger
    `Intents.ALL` is a shortcut provided by interactions.py to enable *every single intent, including privileged intents.* This is very useful while testing bots, **but this shortcut is an incredibly bad idea to use when actually running your bots for use.** As well as adding more strain on the bot (as discussed earlier with normal intents), this is just a bad idea privacy wise: your bot likely does not need to know that much data.

For more information, please visit the API reference about Intents [at this page](/interactions.py/API Reference/API Reference/models/Discord/enums/#interactions.models.discord.enums.Intents).

## Subscribing to Events

After your intents have been properly configured, you can start to listen to events. Say, if you wanted to listen to channels being created in a guild the bot can see, then all you would have to do is this:

```python
from interactions import listen
from interactions.api.events import ChannelCreate

@listen(ChannelCreate)
async def an_event_handler(event: ChannelCreate):
    print(f"Channel created with name: {event.channel.name}")
```

As you can see, the `listen` statement marks a function to receive (or, well, listen/subscribe to) a specific event - we specify which event to receive by passing in the *event object*, which is an object that contains all information about an event. Whenever that events happens in Discord, it triggers our function to run, passing the event object into it. Here, we get the channel that the event contains and send out its name to the terminal.

???+ note "Difference from other Python Discord libraries"
    If you come from some other Python Discord libraries, or even come from older versions of interactions.py, you might have noticed how the above example uses an *event object* - IE a `ChannelCreate` object - instead of passing the associated object with that event - IE a `Channel` (or similar) object - into the function. This is intentional - by using event objects, we have greater control of what information we can give to you.

    For pretty much every event object, the object associated with that event is still there, just as an attribute. Here, the channel is in `event.channel` - you'll usually find the object in other events in a similar format.
    Update events usually use `event.before` and `event.after` too.

While the above is the recommended format for listening to events (as you can be sure that you specified the right event), there are other methods for specifying what event you're listening to:

???+ warning "Event name format for some methods"
    You may notice how some of these methods require the event name to be `all_in_this_case`. The casing itself is called *snake case* - it uses underscores to indicate either a literal space or a gap between words, and exclusively uses lowercase otherwise. To transform an event object, which is in camel case (more specifically, Pascal case), to snake case, first take a look at the letters that are capital, make them lowercase, and add an underscore before those letters *unless it's the first letter of the name of the object*.

    For example, looking at **C**hannel**C**reate, we can see two capital letters. Making them lowercase makes it **c**hannel**c**reate, and then adding an underscore before them makes them **c**hannel**_c**reate (notice how the first letter does *not* have a lowercase before them).

    You *can* add an `on_` prefixed before the modified event name too. For example, you could use both `on_channel_create` and `channel_create`, depending on your preference.

    If you're confused by any of this, stay away from methods that use this type of name formatting.

=== ":one: Type Annotation"
    ```python
    @listen()
    async def an_event_handler(event: ChannelCreate):
        ...
    ```

=== ":two: String in `listen`"
    ```python
    @listen("channel_create")
    async def an_event_handler(event):
        ...
    ```

=== ":three: Function name"
    ```python
    @listen()
    async def channel_create(event):
        ...
    ```

## Other Notes About Events

### No Argument Events

Some events may have no information to pass - the information is the event itself. This happens with some of the internal events - events that are specific to interactions.py, not Discord.

Whenever this happens, you can specify the event to simply not pass anything into the function, as can be seen with the startup event:

```python
from interactions.api.events import Startup

@listen(Startup)
async def startup_func():
    ...
```

If you forget, the library will just pass an empty object to avoid errors.

### Disabling Default Listeners

Some internal events, like `ModalCompletion`, have default listeners that perform niceties like logging the command/interaction logged. You may not want this, however, and may want to completely override this behavior without subclassing `Client`. If so, you can achieve it through `disable_default_listeners`:

```python
from interactions.api.events import ModalCompletion

@listen(ModalCompletion, disable_default_listeners=True)
async def my_modal_completion(event: ModalCompletion):
    print("I now control ModalCompletion!")
```

A lot of times, this behavior is used for custom error tracking. If so, [take a look at the error tracking guide](../25 Error Tracking) for a guide on that.

## Events to Listen To

There are a plethora of events that you can listen to. You can find a list of events that are currently supported through the two links below - every class listened on these two pages are available for you, though be aware that your `Intents` must be set appropriately to receive the event you are looking for.

- [Discord Events](/interactions.py/API Reference/API Reference/events/discord/)
- [Internal Events](/interactions.py/API Reference/API Reference/events/internal/)

### Frequently Used Events

- [Startup](/interactions.py/API Reference/API Reference/events/internal/#interactions.api.events.internal.Startup) is an event, as its name implies, that runs when the bot is first started up - more specifically, it runs when the bot is first ready to do actions. This is a good place to set up tools or libraries that require an asynchronous function.
- [Error](/interactions.py/API Reference/API Reference/events/internal/#interactions.api.events.internal.Error) and its many, *many* subclasses about specific types of errors trigger whenever an error occurs while the bot is running. If you want error *tracking* (IE just logging the errors you get to fix them later on), then [take a look at the error tracking guide](../25 Error Tracking). Otherwise, you can do specific error handling using these events (ideally with `disable_default_listeners` turned on) to provide custom messages for command errors.
- [Component](/interactions.py/API Reference/API Reference/events/internal/#interactions.api.events.internal.Component), [ButtonPressed](/interactions.py/API Reference/API Reference/events/internal/#interactions.api.events.internal.ButtonPressed), [Select](/interactions.py/API Reference/API Reference/events/internal/#interactions.api.events.internal.Select), and [ModalCompletion](/interactions.py/API Reference/API Reference/events/internal/#interactions.api.events.internal.ModalCompletion) may be useful for you if you're trying to respond to component or modal interactions - take a look at the [component guide](../05 Components) or the [modal guide](../06 Modals) for more information.
- [MessageCreate](/interactions.py/API Reference/API Reference/discord/#interactions.api.events.discord.MessageCreate) is used whenever anyone sends a message to a channel the bot can see. This can be useful for automoderation, though note *message content is a privileged intent*, as talked about above. For prefixed/text commands in particular, we already have our own implementation - take a look at them [at this page](../26 Prefixed Commands).
- [GuildJoin](/interactions.py/API Reference/API Reference/events/discord/#interactions.api.events.discord.GuildJoin) and [GuildLeft](/interactions.py/API Reference/API Reference/events/discord/#interactions.api.events.discord.GuildLeft) are, as you can expect, events that are sent whenever the bot joins and leaves a guild. Note that for `GuildJoin`, the event triggers for *every guild on startup* - it's best to have a check to see if the bot is ready through `bot.is_ready` and ignore this event if it isn't.


# Extensions

## Introduction

Your code's getting pretty big and messy being in a single file, huh? Wouldn't it be nice if you could organise your commands and listeners into separate files?

Well let me introduce you to `Extensions`!<br>
Extensions allow you to split your commands and listeners into separate files to allow you to better organise your project.
They also come with the additional benefit of being able to reload parts of your bot without shutting down your bot.

For example, you can see the difference of a bot with and without extensions:

??? Hint "Examples:"
    === "Without Extensions"
        ```python
        from interactions import ActionRow, Button, ButtonStyle, Client, Intents, listen, slash_command
        from interactions.api.events import Component, GuildJoin, MessageCreate, Startup

        bot = Client(intents=Intents.DEFAULT | Intents.MESSAGE_CONTENT)


        @listen(Startup)
        async def on_startup():
            print(f"Ready - this bot is owned by {bot.owner}")


        @listen(GuildJoin)
        async def on_guild_join(event: GuildJoin):
            print(f"Guild joined : {event.guild.name}")


        @listen(MessageCreate)
        async def on_message_create(event: MessageCreate):
            print(f"message received: {event.message}")


        @listen()
        async def on_component(event: Component):
            ctx = event.ctx
            await ctx.edit_origin(content="test")


        @slash_command()
        async def multiple_buttons(ctx):
            await ctx.send(
                "2 buttons in a row",
                components=[
                    Button(style=ButtonStyle.BLURPLE, label="A blurple button"),
                    Button(style=ButtonStyle.RED, label="A red button"),
                ],
            )


        @slash_command()
        async def action_rows(ctx):
            await ctx.send(
                "2 buttons in 2 rows, using nested lists",
                components=[
                    [Button(style=ButtonStyle.BLURPLE, label="A blurple button")],
                    [Button(style=ButtonStyle.RED, label="A red button")],
                ],
            )


        @slash_command()
        async def action_rows_more(ctx):
            await ctx.send(
                "2 buttons in 2 rows, using explicit action_rows lists",
                components=[
                    ActionRow(Button(style=ButtonStyle.BLURPLE, label="A blurple button")),
                    ActionRow(Button(style=ButtonStyle.RED, label="A red button")),
                ],
            )


        bot.start("token")
        ```

    === "With Extensions"
        ```python
        # File: `main.py`
        from interactions import Client, Intents, listen
        from interactions.api.events import Component, GuildJoin, MessageCreate, Startup

        bot = Client(intents=Intents.DEFAULT | Intents.MESSAGE_CONTENT)


        @listen(Startup)
        async def on_startup():
            print(f"Ready - this bot is owned by {bot.owner}")


        @listen(GuildJoin)
        async def on_guild_join(event: GuildJoin):
            print(f"Guild joined : {event.guild.name}")


        @listen(MessageCreate)
        async def on_message_create(event: MessageCreate):
            print(f"message received: {event.message}")


        @listen()
        async def on_component(event: Component):
            ctx = event.ctx
            await ctx.edit_origin(content="test")


        bot.load_extension("test_components")
        bot.start("token")
        ```
        ```python

        # File: `test_components.py`

        from interactions import ActionRow, Button, ButtonStyle, Extension, slash_command


        class ButtonExampleSkin(Extension):
            @slash_command()
            async def multiple_buttons(self, ctx):
                await ctx.send(
                    "2 buttons in a row",
                    components=[
                        Button(style=ButtonStyle.BLURPLE, label="A blurple button"),
                        Button(style=ButtonStyle.RED, label="A red button"),
                    ],
                )


            @slash_command()
            async def action_rows(self, ctx):
                await ctx.send(
                    "2 buttons in 2 rows, using nested lists",
                    components=[
                        [Button(style=ButtonStyle.BLURPLE, label="A blurple button")],
                        [Button(style=ButtonStyle.RED, label="A red button")],
                    ],
                )


            @slash_command()
            async def action_rows_more(self, ctx):
                await ctx.send(
                    "2 buttons in 2 rows, using explicit action_rows lists",
                    components=[
                        ActionRow(Button(style=ButtonStyle.BLURPLE, label="A blurple button")),
                        ActionRow(Button(style=ButtonStyle.RED, label="A red button")),
                    ],
                )
        ```

Sounds pretty good right? Well, let's go over how you can use them:

## Basic Usage

### Setup

Extensions are effectively just another Python file that contains a class that inherits from an object called `Extension`,
inside this extension.

For example, this is a valid extension file:

```python
from interactions import Extension

class MyExtension(Extension):
    pass
```

??? note "Differences from Other Python Discord Libraries"
    If you come from another Python Discord library, you might have seen that there's no `__init__` and `setup` function in this example.
    They still do exist as functions you *can* use (as discussed later), but interactions.py will do the appropriate logic to handle extensions
    without either of the two.

    For example, the following does the exact same thing as the above extension file:

    ```python
    from interactions import Extension

    class MyExtension(Extension):
        def __init__(self, bot):
            self.bot = bot

    def setup(bot):
        # yes, the bot does not need to do any special logic - you just need to pass it into the extension
        MyExtension(bot)
    ```

### Events and Commands

You probably want extensions to do a little bit more than just exist though. Most likely, you want some events and commands
in here. Thankfully, they're relatively simple to do. Expanding on the example a bit, a slash command looks like this:

```python
from interactions import Extension, slash_command, SlashContext

class MyExtension(Extension):
    @slash_command()
    async def test(self, ctx: SlashContext):
        await ctx.send("Hello world!")
```

As you can see, they're almost identical to how you declare slash commands in your main bot file, even using the same decorator.
The only difference is the `self` variable - this is the instance of the extension that the command is being called in, and is
standard for functions inside of classes. Events follow a similar principal.

interactions.py will automatically add all commands and events to the bot when you load the extension (discussed later),
so you don't need to worry about that.

#### Accessing the Bot

When an extension is loaded, the library automatically sets the `bot` for you. With this in mind, you can access your client using `self.bot`.
Using `self.client` also works - they are just aliases to each other.

```python
class MyExtension(Extension):
    @slash_command()
    async def test(self, ctx: SlashContext):
        await ctx.send(f"Hello, I'm {self.bot.user.mention}!")
```

This also allows you to share data between extensions and the main bot itself. `Client` allows storing data in unused attributes,
so you can do something like this:

```python
from interactions import Client

# main.py
bot = Client(...)
bot.my_data = "Hello world"

# extension.py
class MyExtension(Extension):
    @slash_command()
    async def test(self, ctx: SlashContext):
        await ctx.send(f"My data: {self.bot.my_data}!")
```

### Loading the Extension

Now that you've got your extension, you need to load it.

Let's pretend the extension is in a file called `extension.py`, and it looks like the command example:

```python
from interactions import Extension, slash_command, SlashContext

class MyExtension(Extension):
    @slash_command()
    async def test(self, ctx: SlashContext):
        await ctx.send("Hello world!")
```

Now, let's say you have a file called `main.py` in the same directory that actually has the bot in it:

```python
bot = Client(...)
bot.start("token")
```

To load the extension, you just need to use `bot.load_extension("filename.in_import_style")` before `bot.start`. So, in this case, it would look like this:

```python
bot = Client(...)
bot.load_extension("extension")
bot.start("token")
```

And that's it! Your extension is now loaded and ready to go.

#### "Import Style"

In the example above, the filename is passed to `load_extension` without the `.py` extension. This is because interactions.py actually does an
*import* when loading the extension, so whatever string you give it needs to be a valid Python import path. This means that if you have a file structure like this:

```
main.py
exts/
    extension.py
```

You would need to pass `exts.extension` to `load_extension`, as that's the import path to the extension file.

#### Reloading and Unloading Extensions

You can also reload and unload extensions. To do this, you use `bot.reload_extension` and `bot.unload_extension` respectively.

```python
bot.reload_extension("extension")
bot.unload_extension("extension")
```

Reloading and unloading extensions allows you to edit your code without restarting the bot, and to remove extensions you no longer need.
For example, if you organize your extensions so that moderation commands are in one extension, you can reload that extension (and so only moderation-related commands)
as you edit them.

### Initialization

You may want to do some logic to do when loading a specific extension. For that, you can add the `__init__` method, which takes a `Client` instance, in your extension:

```python
class MyExtension(Extension):
    def __init__(self, bot):
        # do some initialization here
        pass
```

#### Asynchronous Initialization

As usual, `__init__` is synchronous. This may pose problems if you're trying to do something asynchronous in it, so there are various ways of solving it.

If you're okay with only doing the asynchronous logic as the bot is starting up (and never again), there are two methods:

=== "`async_start`"
    ```python
    class MyExtension(Extension):
        async def async_start(self):
            # do some initialization here
            pass
    ```

=== "`Startup` Event"
    ```python
    from interactions.api.events import Startup

    class MyExtension(Extension):
        @event(Startup)
        async def startup(self):
            # do some initialization here
            pass
    ```

If you want to do the asynchronous logic every time the extension is loaded, you'll need to use `asyncio.create_task`:

```python
import asyncio

class MyExtension(Extension):
    def __init__(self, bot):
        asyncio.create_task(self.async_init())

    async def async_init(self):
        # do some initialization here
        pass
```

!!! warning "Warning about `asyncio.create_task`"
    `asyncio.create_task` only works *if there is an event loop.* For the sake of simplicity we won't discuss what that is too much,
    but the loop is only created when `asyncio.run()` is called (as it is in `bot.start()`). This means that if you call `asyncio.create_task`
    before `bot.start()`, it will not work. If you need to do asynchronous logic before the bot starts, you'll need to load the extension
    in an asynchronous function and use `await bot.astart()` instead of `bot.start()`.

    For example, this format of loading extensions will allow you to use `asyncio.create_task`:

    ```python
    bot = Client(...)

    async def main():
        # event loop made!
        bot.load_extension("extension")
        await bot.astart("token")

    asyncio.run(main())
    ```

### Cleanup

You may have some logic to do while unloading a specific extension. For that, you can override the `drop` method in your extension:

```python
class MyExtension(Extension):
    def drop(self):
        # do some cleanup here
        super().drop()  # important - this part actually does the unloading
```

The `drop` method is synchronous. If you need to do something asynchronous, you can create a task with `asyncio` to do it:

???+ note "Note about `asyncio.create_task`"
    Usually, there's always an event loop running when unloading an extension (even when the bot is shutting down), so you can use `asyncio.create_task` without any problems.
    However, if you are unloading an extension before `asyncio.run()` has called, the warning from above applies.

```python
import asyncio

class MyExtension(Extension):
    def drop(self):
        asyncio.create_task(self.async_drop())
        super().drop()

    async def async_drop(self):
        # do some cleanup here
        pass
```

## Advanced Usage

### Loading All Extensions In a Folder

Sometimes, you may have a lot of extensions contained in one folder. Writing them all out is both time consuming and not very scalable, so you may want an easier way to load them.

If your folder with all of your extensions is "flat" (only containing Python files for extensions and no subfolders), then your best bet is to use [`pkgutil.iter_modules`](https://docs.python.org/3/library/pkgutil.html#pkgutil.iter_modules) and a for loop:
```python
import pkgutil

# replace "exts" with your folder name
extension_names = [m.name for m in pkgutil.iter_modules(["exts"], prefix="exts.")]
for extension in extension_names:
    bot.load_extension(extension)
```

`iter_modules` finds all modules (which include Python extension files) in the directories provided. By default, this *just* returns the module/import name without the folder name, so we need to add the folder name back in through the `prefix` argument.
Note how the folder passed and the prefix are basically the same thing - the prefix just has a period at the the end.

If your folder with all of your extensions is *not* flat (for example, if you have subfolders in the extension folder containing Python files for extensions), you'll likely want to use [`glob.glob`](https://docs.python.org/3/library/glob.html#glob.glob) instead:
```python
import glob

# replace "exts" with your folder name
ext_filenames = glob.glob("exts/**/*.py")
extension_names = [filename.removesuffix(".py").replace("/", ".") for filename in ext_filenames]
for extension in extension_names:
    bot.load_extension(extension)
```

Note that `glob.glob` returns the *filenames* of all files that match the pattern we provided. To turn it into a module/import name, we need to remove the ".py" suffix and replace the slashes with periods.
On Windows, you may need to replace the slashes with backslashes instead.

???+ note "Note About Loading Extensions From a File"
    While these are two possible ways, they are by no means the *only* ways of finding all extensions in the folder and loading them. Which method is best method depends on your use case and is purely subjective.


### The `setup`/`teardown` Function

You may have noticed that the `Extension` in the extension file is simply just a class, with no way of loading it. interactions.py is smart enough to detect `Extension` subclasses
and use them when loading from a file, but if you want more customization when loading an extension, you'll need to use the `setup` function.

The `setup` function should be *outside* of any `Extension` subclass, and takes in the bot instance, like so:

```python
class MyExtension(Extension):
    ...

def setup(bot):
    # insert logic here
    MyExtension(bot)
```

Here, the `Extension` subclass is initialized inside the `setup` function, and does not need to do any special function to add the extension in beyond being created using the instance.

A similar function can be used for cleanup, called `teardown`. It takes no arguments, and should be outside of any `Extension` subclass, like so:

```python
class MyExtension(Extension):
    ...

def teardown():
    # insert logic here
    pass
```

You usually do not need to worry about unloading the specific extensions themselves, as interactions.py will do that for you.

### Passing Arguments to Extensions

If you would like to pass more than just the bot while initializing an extension, you can pass keyword arguments to the `load_extension` method:

```python
class MyExtension(Extension):
    def __init__(self, bot, some_arg: int = 0):
        ...

bot.load_extension("extension", some_arg=5)
```

If you're using a `setup` function, the argument will be passed to that function instead, so you'll need to pass it to the `Extension` subclass yourself:

```python
class MyExtension(Extension):
    ...

def setup(bot, some_arg: int = 0):
    MyExtension(bot, some_arg)
```

## Extension-Wide Checks

Sometimes, it is useful to have a check run before running any command in an extension. Thankfully, all you need to do is use `add_ext_check`:

```python
class MyExtension(Extension):
    def __init__(self, bot: Client):
        self.add_ext_check(self.a_check)

    async def a_check(ctx: SlashContext) -> bool:
        return bool(ctx.author.name.startswith("a"))

    @slash_command(...)
    async def my_command(...):
        # only ran with people whose names start with an a
        ...
```

### Global Checks

You may want to have a check that runs on every command in a bot. If all of your commands are in extensions (a good idea), you can use
a custom subclass of `Extension` to do it:

```python
# file 1
class CustomExtension(Extension):
    def __init__(self, client: Client):
        self.client = client
        self.add_ext_check(self.a_check)

    async def a_check(ctx: InteractionContext) -> bool:
        return bool(ctx.author.name.startswith("a"))

# file 2
class MyExtension(CustomExtension):
    @slash_command(...)
    async def my_command(...):
        ...
```

### Pre And Post Run Events

Pre- and post-run events are similar to checks. They run before and after a command is invoked, respectively:

```python
from interactions import BaseContext

class MyExtension(Extension):
    def __init__(self, bot: Client):
        self.add_extension_prerun(self.pre_run)
        self.add_extension_postrun(self.post_run)

    async def pre_run(ctx: BaseContext):
        print(f"Command started at: {datetime.datetime.now()}")

    async def post_run(ctx: BaseContext):
        print(f"Command done at: {datetime.datetime.now()}")

    @slash_command(...)
    async def my_command(...):
        # pre and post run will be ran before/after this command
        ...
```

### Extension-Wide Error Handlers

Sometimes, you may want to have a custom error handler for all commands in an extension. You can do this by using `set_extension_error`:

```python
class MyExtension(Extension):
    def __init__(self, bot: Client):
        self.set_extension_error(self.error_handler)

    async def error_handler(self, error: Exception, ctx: BaseContext):
        # handle the error here
        ...
```

??? note "Error Handling Priority"
    Only one error handler will run. Similar to CSS, the most specific handler takes precedence.
    This goes: command error handlers -> extension -> listeners.

### Extension Auto Defer

You may want to automatically defer all commands in that extension. You can do this by using `add_ext_auto_defer`:

```python
class MyExtension(Extension):
    def __init__(self, bot: Client):
        self.add_ext_auto_defer(enabled=True, ephemeral=False, time_until_defer=0.5)
```

??? note "Auto Defer Handling Priority"
    Similar to errors, only one auto defer will be run, and the most specific auto defer takes precendence.
    This goes: command auto defer -> extension -> bot.


# Live Patching

interactions.py has a few built-in extensions that add some features, primarily for debugging. One of these extensions that you can enable separately is to add [`jurigged`](https://github.com/breuleux/jurigged) for live patching of code.

## How to enable

```py
bot.load_extension("interactions.ext.jurigged")
```

That's it! The extension will handle all of the leg work, and all you'll notice is that you have more messages in your logs (depending on the log level).

## What is jurigged?

`jurigged` is a library written to allow code hot reloading in Python. It allows you to edit code and have it automagically be updated in your program the next time it is run. The code under the hood is extremely complicated, but the interface to use it is relatively simple.

## How is this useful?

interactions.py takes advantage of jurigged to reload any and all commands that were edited whenever a change is made, allowing you to have more uptime with while still adding/improving features of your bot.

## It's not working inside Docker!
To make `jurigged` work inside Docker container, you need to mount the directory you're working in as a volume in the container (pointing to the code directory inside the container).

Additionally, you need to initialize the `jurigged` extension with the `poll` keyword argument set to `True`:

```py
bot.load_extension("interactions.ext.jurigged", poll=True)
```


# Voice Support

So you want to start playing some 🎵tunes🎶 in voice channels? Well let's get that going for you.

=== ":simple-windows: Windows"

    First you're going to want to get the voice dependencies installed:
    ```
    pip install discord.py-interactions[voice]
    ```

    Then you'll need to download [FFmpeg](https://ffmpeg.org) and place it in your project directory or PATH.

    Now you've got those; let's make a simple play command to get you started.

=== ":simple-linux: Linux"

    First you're going to want to get the voice dependencies installed:
    ```
    pip install discord.py-interactions[voice]
    ```

    Then you'll need to install the following packages:
    [libnacl](https://github.com/saltstack/libnacl), [libffi](https://github.com/libffi/libffi), and [FFmpeg](https://ffmpeg.org)

    :simple-debian: For debian based distros:
    ```
    sudo apt install ffmpeg libffi-dev libnacl-dev
    ```
    :simple-archlinux: For arch based distros:
    ```
    sudo pacman -S ffmpeg libffi libnacl
    ```
    :simple-fedora: For fedora based distros:
    ```
    sudo dnf install ffmpeg libffi-devel libsodium-devel
    ```

    If you get an error about "Could not find opus library," your distro may not have libopus installed. You'll need to find documentation for your distro on how to install it.


    Now you've got those; let's make a simple play command to get you started.

```python
import interactions
from interactions.api.voice.audio import AudioVolume


@interactions.slash_command("play", "play a song!")
@interactions.slash_option("song", "The song to play", 3, True)
async def play(self, ctx: interactions.SlashContext, song: str):
    if not ctx.voice_state:
        # if we haven't already joined a voice channel
        # join the authors vc
        await ctx.author.voice.channel.connect()

    # Get the audio using YTDL
    audio = await AudioVolume(song)
    await ctx.send(f"Now Playing: **{song}**")
    # Play the audio
    await ctx.voice_state.play(audio)
```

Now just join a voice channel, and type run the "play" slash command with a song of your choice.

Congratulations! You've got a music-bot.

## But what about local music?

If you want to play your own files, you can do that too! Create an `AudioVolume` object and away you go.

!!! note
    If your audio is already encoded, use the standard `Audio` object instead. You'll lose volume manipulation, however.

```python
import interactions
from interactions.api.voice.audio import AudioVolume


@interactions.slash_command("play", "play a song!")
async def play_file(ctx: interactions.SlashContext):
    audio = AudioVolume("some_file.wav")
    await ctx.voice_state.play(audio)
```

Check out [Active Voice State](/interactions.py/API Reference/API Reference/models/Internal/active_voice_state/) for a list of available methods and attributes.

# Voice Recording

So you've got a bot that can play music, but what about recording? Well, you're in luck! We've got you covered.

Let's start with a simple example:

```python
import asyncio
import interactions

@interactions.slash_command("record", "record some audio")
async def record(ctx: interactions.SlashContext):
    voice_state = await ctx.author.voice.channel.connect()

    # Start recording
    await voice_state.start_recording()
    await asyncio.sleep(10)
    await voice_state.stop_recording()
    await ctx.send(files=[interactions.File(file, file_name="user_id.mp3") for user_id, file in voice_state.recorder.output.items()])
```
This code will connect to the author's voice channel, start recording, wait 10 seconds, stop recording, and send a file for each user that was recorded.

But what if you didn't want to use `mp3` files? Well, you can change that too! Just pass the encoding you want to use to `start_recording`.

```python
await voice_state.start_recording(encoding="wav")
```

For a list of available encodings, check out Recorder's [documentation](/interactions.py/API Reference/API_Communication/voice/recorder.md)

Are you going to be recording for a long time? You are going to want to write the files to disk instead of keeping them in memory. You can do that too!

```python
await voice_state.start_recording(output_dir="folder_name")
```
This will write the files to the folder `folder_name` in the current working directory, please note that the library will not create the folder for you, nor will it delete the files when you're done.


# Localising

So your bot has grown, and now you need to ~~localize~~ localise your bot. Well thank god we support localisation then, huh?

To clarify; localisation is a feature of application commands that discord offers,
this means the same command will have different names and descriptions depending on the user's locale settings.

# How its made:

Let's take this nice and simple `hello` command

```python
import interactions

@interactions.slash_command(name="hello")
async def hello_cmd(ctx: interactions.SlashContext):
    await ctx.send(f"Hello {ctx.author.display_name}")
```
This command was immensely popular, and now we have some 🇫🇷 French users. Wouldn't it be nice if we could speak their language.

```python
import interactions
from interactions import LocalisedName

@interactions.slash_command(name=LocalisedName(english_us="hello", french="salut"))
async def hello_cmd(ctx: interactions.SlashContext):
    await ctx.send(f"Hello {ctx.author.display_name}")
```
All we need to do is set the field to a `Localised` object, and interactions.py and discord wil handle the rest for you.
For extra flavour lets make this command more dynamic.

```python
import interactions
from interactions import LocalisedName

@interactions.slash_command(name=LocalisedName(english_us="hello", french="salut"))
async def hello_cmd(ctx: interactions.SlashContext):
    await ctx.send(f"{ctx.invoked_name} {ctx.author.display_name}")
```
Simply by changing `"hello"` to `ctx.invoked_name` the command will always use whatever the user typed to greet them.
If you want to know what locale the user is in, simply use `ctx.locale`.


This will work for any object with a `name` or `description` field. Simply use `LocalisedDesc` instead for descriptions.
For example, you can localise options, choices, and subcommands.


# Error Tracking

So, you've finally got your bot running on a server somewhere.  Chances are, you're not checking the console output 24/7, looking for exceptions.

You're going to want to have some way of tracking if errors occur.

# Sending inline tracebacks

By default, if a command throws an uncaught exception, it'll send the traceback to the user.  This is very useful when in development, but doesn't help you once you've gone public, and might not be in the same servers as your errors.  Non-technical users may also find it confusing to see trackbacks instead of user-friendly error messages.

If you wish to turn this off, create your client with `Client(..., send_command_tracebacks=False)`


# The simple and dirty method

!!! Please don't actually do this.

The most obvious solution is to think "Well, I'm writing a Discord Bot.  Why not send my errors to a discord channel?"

```python
from interactions.api.events import Error

@listen()
async def on_error(error: Error):
    await bot.get_channel(LOGGING_CHANNEL_ID).send(f"```\n{error.source}\n{error.error}\n```")
```

And this is great when debugging.  But it consumes your rate limit, can run into the 2000 character message limit, and won't work on shards that don't contain your personal server.  It's also very hard to notice patterns and can be noisy.

# So what should I do instead?

interactions.py contains built-in support for Sentry.io, a cloud error tracking platform.

To enable it, call `bot.load_extension('interactions.ext.sentry', token=SENTRY_TOKEN)` as early as possible in your startup. (Load it before your own extensions, so it can catch intitialization errors in those extensions)

# What does this do that vanilla Sentry doesn't?

We add some [tags](https://docs.sentry.io/platforms/python/enriching-events/tags/) and [contexts](https://docs.sentry.io/platforms/python/enriching-events/context/) that might be useful, and filter out some internal-errors that you probably don't want to see.


# Creating Prefixed Commands

Prefixed commands, called by Discord as "text commands" and sometimes called "message commands" (not to be confused with Context Menu Message Commands), are commands that are triggered when a user sends a normal message with a designated "prefix" in front of them.

??? note "Naming"
    While Discord themselves has used "text commands" to refer to these, we disagree with this naming. We think it is confusing, especially when referring to how Discord refers to slash commands (chat input commands). Thus, this library will use "prefixed commands", both in code and for its documentation.

While slash commands have been released, and is typically the way you should be making commands these days, there are many cases where the "legacy" commands may want to be kept due to various reasons, like wanting to use types not well-supported by Discord or to allow for greater flexibility for permission handling.

Whatever the reason is, `interactions.py` has an extensive yet familiar prefixed command architecture ready to be used via a built-in extension.

## Setup

Because prefixed commands are in their own extension, some setup is required. It usually is as simple as putting something like this in your main bot file:

```python
from interactions import Client, Intents
from interactions.ext import prefixed_commands

# guild messages are included in the default intents ipy uses
# if you wish for the prefix to be anything but mentioning the bot,
# guild message content will also be required
client = Client(..., intents=Intents.GUILD_MESSAGES | ...)
prefixed_commands.setup(client)
```

By default, this will set up the bot to use prefixed commands and use mentioning the bot as the prefix (IE @bot hello).
If you wish to change this, you have two options in `setup`:

- If you want the bot to response to a static set of prefixes, you can use the `default_prefix` parameter to set the prefix to either a singular prefix or a list of prefixes.
- If you want to dynamically determine which prefix(es) the bot should return to (say, based on the guild that the command is being run in), you can use the `generate_prefixes` parameter. The parameter takes in an asynchronous function that takes in the `Client` and a `Message`, and returns a prefix or a list of prefixes.

## Your First Prefixed Command

To create a prefixed command, simply define an asynchronous function and use the `@prefixed_command()` (from `interactions.ext.prefixed_commands`) decorator above it.

```python
from interactions.ext.prefixed_commands import prefixed_command, PrefixedContext

@prefixed_command(name="my_command")
async def my_command_function(ctx: PrefixedContext):
    await ctx.reply("Hello world!")
```

???+ note "Command Name"
    If `name` is not specified, `interactions.py` will automatically use the function's name as the command's name.

If the bot's prefix was set to `!`, then a user could invoke it like so:

![Hello World!](../images/PrefixedCommands/FirstCommand.png "The above command running.")

## Subcommands

Subcommands are rather simple, too:

```python
@prefixed_command()
async def base_command(ctx: PrefixedContext):
    await ctx.reply("This is the base command.")

@base_command.subcommand()
async def subcommand(ctx: PrefixedContext):
    await ctx.reply("This is a subcommand.")
```

A user can use them like so:

![Subcommands](../images/PrefixedCommands/Subcommands.png "Both the base command and the subcommand running.")

## Parameters

Often, when using prefixed commands, you typically want to parse what the user says into separated parameters/arguments. This can be done easily in this library using a Python-esque syntax.

For example, to make a command that takes in one argument, we can do:
```python
@prefixed_command()
async def test(ctx: PrefixedContext, arg):
    await ctx.reply(arg)
```

When a user uses the command, all they simply need to do is pass a word after the command:

![One Parameter](../images/PrefixedCommands/OneParamNoQuotes.png "The above running with the argument: hello!")

If the user wishes to use multiple words in an argument like this, they can wrap it in quotes like so:

![One Parameter With Quotes](../images/PrefixedCommands/OneParamWithQuotes.png "The above running with the argument: "hello world!"")

!!! warning "Forgetting Quotes"
    If a user forgets or simply does not wrap multiple words in an argument in quotes, the library will only use the first word for the argument and ignore the rest.

    ![Don't Forget Quotes](../images/PrefixedCommands/DontForgetQuotes.png "The above running with the argument hello world! - the bot only outputs hello.")

You can add as many parameters as you want to a command:
```python
@prefixed_command()
async def test(ctx: PrefixedContext, arg1, arg2):
    await ctx.reply(f"Arguments: {arg1}, {arg2}.")
```

![Two Parameters](../images/PrefixedCommands/TwoParams.png "The above running with the arguments: one two")

### Variable and Consume Rest Arguments

There may be times where you wish for an argument to be able to have multiple words without wrapping them in quotes. There are two ways of approaching this.

#### Variable

If you wish to get a list (or more specifically, a tuple) of words for one argument, or simply want an undetermined amount of arguments for a command, then you should use a *variable* argument:

=== ":one: Tuple Argument"
    ```python
    @prefixed_command()
    async def test(ctx: PrefixedContext, args: tuple[str, ...]):
        await ctx.reply(f"{len(args)} arguments: {', '.join(args)}")
    ```

=== ":two: Variable Positional Argument"
    ```python
    @prefixed_command()
    async def test(ctx: PrefixedContext, *args):
        await ctx.reply(f"{len(args)} arguments: {', '.join(args)}")
    ```

The result looks something like this:

![Variable Parameter](../images/PrefixedCommands/VariableParam.png "The above running with the arguments: hello there world "how are you?"")

Notice how the quoted words are still parsed as one argument in the tuple.

#### Consume Rest

If you simply wish to take in the rest of the user's input as an argument, you can use a consume rest argument, like so:

=== ":one: ConsumeRest Alias"
    ```python
    from interactions import ConsumeRest

    @prefixed_command()
    async def test(ctx: PrefixedContext, arg: ConsumeRest[str]):
        await ctx.reply(arg)
    ```

=== ":two: Keyword-only Argument"
    ```python
    @prefixed_command()
    async def test(ctx: PrefixedContext, *, arg):
        await ctx.reply(arg)
    ```

The result looks like this:

![Consume Rest Parameter](../images/PrefixedCommands/ConsumeRestParam.png "The above running with the arguments: hello world!")

???+ note "Quotes"
    If a user passes quotes into consume rest argument, then the resulting argument will have said quotes.

    ![Consume Rest Quotes](../images/PrefixedCommands/ConsumeRestWithQuotes.png "The above running with the arguments: "hello world!"")

!!! warning "Parser ambiguities"
    Due to parser ambiguities, you can *only* have either a single variable or consume rest argument.

## Typehinting and Converters

### Basic Types

Parameters, by default, are assumed to be strings, since `Message.content`, the content used for prefixed commands, is one. However, there are many times where you want to have a parameter be a more specific type, like an integer or boolean.

`interactions.py` provides an easy syntax to do so:

```python
@prefixed_command()
async def test(ctx: PrefixedContext, an_int: int, a_float: float):
    await ctx.reply(str(an_int + a_float))
```

![Basic Type Conversion](../images/PrefixedCommands/BasicTypeConversion.png "The above running with the arguments: 1 2.5")

Words/arguments will automatically be converted to the specified type. If `interactions.py` is unable to convert it (a user could easily pass a letter into `an_int`), then it will raise a `BadArgument` error, which can be handled by an error handler. Error handling is handled similarly to how it is handled with [slash commands](../03 Creating Commands).

You can even pass in a function for parameters:

```python
def to_upper(arg: str):
    return arg.upper()

@prefixed_command()
async def test(ctx: PrefixedContext, uppered: to_upper):
    await ctx.reply(uppered)
```

![Function Conversion](../images/PrefixedCommands/FunctionConversion.png "The above running with the arguments: hello!")

??? note "Functions"
    If functions are used as arguments, they can either have one parameter (which is the passed argument as a string) or two parameters (which are the context and the argument).
    They can also be asynchronous or synchronous.
    Also, your typechecker will likely complain about this. You can ignore it for `interactions.py`.

#### Booleans

Booleans, unlike other basic types, are handled somewhat differently, as using the default `bool` converter would make any non-empty argument `True`. It is instead evaluated as so:

```python
if lowered in {"yes", "y", "true", "t", "1", "enable", "on"}:
    return True
elif lowered in {"no", "n", "false", "f", "0", "disable", "off"}:
    return False
```

### Converters

Converters work much in the same way as they do for other commands; see [the guide for converters for reference](../08 Converters).

There are a few specific converters that only work with prefixed commands due to their nature, however.

#### Discord Converters

Prefixed commands can be typehinted with some Discord models, like so:

```python
from interactions import Member

@prefixed_command()
async def poke(ctx: PrefixedContext, target: Member):
    await ctx.reply(f"{target.mention}, you got poked by {ctx.author.mention}!")
```

The argument here will automatically be converted into a `Member` object:

![Discord Model Conversion](../images/PrefixedCommands/DiscordModelConversion.png "The above running with a user passed in.")

A table of supported objects and their converters can be found [here](../08 Converters#discord-model-converters). You may use the Discord model itself in your command for prefixed commands, just like the above, and their respective converter will be used under the hood.

#### `typing.Union`

`typing.Union` allows for a parameter/argument to be of multiple types instead of one. `interactions.py` will attempt to convert a given argument into each type specified (starting from the first one), going down the "list" until a valid match is found.

For example, the below will try to convert an argument to a `GuildText` first, then a `User` if it cannot do so.

```python
from typing import Union
from interactions import GuildText, User

@prefixed_command()
async def union(ctx: PrefixedContext, param: Union[GuildText, User]):
    await ctx.reply(str(param))
```

Using `|` for specifying a union is also supported, if you prefer it:
```python
@prefixed_command()
async def union(ctx: PrefixedContext, param: GuildText | User):
    await ctx.reply(str(param))
```

![Union Conversion](../images/PrefixedCommands/UnionConversion.png "The above running twice, with a channel passed the first time and a user the second time.")

#### `typing.Optional`

Usually, `Optional[OBJECT]` is an alias for `Union[OBJECT, None]` - it indicates the parameter can be passed `None` or an instance of the object itself. It means something slightly different here, however.

If a parameter is marked as `Optional`, then the command handler will try converting it to the type inside of it, defaulting to either `None` or a default value, if found. A similar behavior is done is the value has a default value, regardless of if it is marked with `Optional` or not.

For example, you could use the following code:

```python
from typing import Optional

@prefixed_command()
async def ban(ctx: PrefixedContext, member: Member, delete_message_days: Optional[int] = 0, *, reason: str):
    await member.ban(delete_message_days=delete_message_days, reason=reason)
    await ctx.reply(f"Banned {member.mention} for {reason}. Deleted {delete_message_days} days of their messages.")
```

And if a user omits the `delete_message_days` parameter, it would act as so:

![Optional Conversion](../images/PrefixedCommands/OptionalConversion.png "The above running, banning a user without specifying delete_message_days.")

#### `typing.Literal`

`typing.Literal` specifies that a parameter *must* be one of the values in the list. `interactions.py` also forces that here (though this only works with values of basic types, like `str` or `int`):

```python
from typing import Literal

@prefixed_command()
async def one_or_two(ctx: PrefixedContext, num: Literal[1, 2]):
    await ctx.reply(str(num))
```

![Literal Conversion](../images/PrefixedCommands/LiteralConversion.png "The above running with the arguments: 1")

#### `Greedy`

The `Greedy` class, included in this library, specifies `interactions.py` to keep converting as many arguments as it can until it fails to do so. For example:

```python
from interactions.ext.prefixed_commands import Greedy

@prefixed_command()
async def slap(ctx: PrefixedContext, members: Greedy[Member]):
    slapped = ", ".join(x.display_name for x in members)
    await ctx.reply(f"{slapped} just got slapped!")
```

![Greedy Conversion](../images/PrefixedCommands/GreedyConversion.png "The above running with multiple users as the arguments.")

!!! warning "Greedy Warnings"
    `Greedy` does *not* default to being optional. You *must* specify that it is by giving it a default value or wrapping it with `Optional`.
    `Greedy`, `str`, `None`, `Optional` are also not allowed as parameters in `Greedy`.
    `Greedy` cannot be used as a variable or keyword-only argument.

## Help Command

There is no automatically added help command in `interactions.py`. However, you can use `PrefixedHelpCommand` to create one with ease. Using it looks like so:

```python
from interactions.ext.prefixed_command.help import PrefixedHelpCommand

# There are a variety of options - adjust them to your liking!
help_cmd = PrefixedHelpCommand(bot, ...)
help_cmd.register()
```

With the default options, the result looks like:

![Help Command](../images/PrefixedCommands/HelpCommand.png "The help command running.")

## Other Notes
- Checks, cooldowns, and concurrency all work as-is with prefixed commands.
- Prefixed commands use a different method to process `Converter`s compared to slash commands. While they should roughly give the same result, they may act slightly differently.
- All prefixed commands use `PrefixedContext`, which contains useful information based on the current instance of the command.


# Pagination

> Pagination, also known as paging, is the process of dividing a document into discrete pages, either electronic pages or printed pages.

We've all hit that point where Discord won't let you send enough characters, at that point you can either flood the channel with multiple messages, or you can start paginating your messages.

interactions.py comes builtin with a pagination utility that splits your messages up into pages, which your user can navigate through.

![Paginator example](../images/paginator%20example.png)

To use it, you only need 3 lines.

```python
from interactions.ext.paginators import Paginator

paginator = Paginator.create_from_string(bot, your_content, page_size=1000)
await paginator.send(ctx)
```

But let's say you have fancy embedded content you want to use. Well don't worry, interactions.py can handle that too:
```python
embeds = [Embed("Page 1 content"), Embed("Page 2 embed"), Embed("Page 3 embed"), Embed("Page 4 embed")]
paginator = Paginator.create_from_embeds(bot, *embeds)
```

Paginators are configurable, you can choose which buttons show, add timeouts, add select menu navigation, and even add callbacks. To see your options, check out their documentation [here](/interactions.py/API Reference/API Reference/ext/paginators).


# Tasks

Tasks are background processes that can be used to asynchronously run code with a specified trigger.

## How They Work

Tasks work by creating an `asyncio.Task` to run a loop to check if the task is ready to be run based on the provided trigger. Using them is fairly easy, and the easiest way is via **Decorators**.

=== ":one: Decorators"
    Decorators are by far the easier way to run tasks, with very simple syntax to get started.

    ```python
    from interactions import Task, IntervalTrigger

    @Task.create(IntervalTrigger(minutes=10)) # (1)!
    async def print_every_ten():
        print("It's been 10 minutes!")
    ```
    { .annotate }

    1. This will create a task that runs every 10 minutes

=== ":two: Manual Registration"
    You can also manually register tasks

    ```python
    from interactions import Task, IntervalTrigger

    async def print_every_ten():
        print("It's been 10 minutes!")

    task = Task(print_every_ten, IntervalTrigger(minutes=10))
    ```

By default, there are a few triggers available to the user.

=== ":one: IntervalTrigger"

    These triggers run every set interval.

    ```python
    from interactions import Task, IntervalTrigger

    @Task.create(IntervalTrigger(minutes=10))
    async def print_every_ten():
        print("It's been 10 minutes!")
    ```

=== ":two: DateTrigger"

    These triggers are similar to IntervalTriggers, but instead run when a specified datetime is reached.

    ```python
    from datetime import datetime, timedelta
    from interactions import Task, DateTrigger

    future = datetime.strptime("%d-%m-%Y", "01-01-2100") # (1)!

    @Task.create(DateTrigger(future)) # (2)!
    async def new_century():
        print("Welcome to the 22nd Century!")
    ```
    { .annotate }

    1. This create a `datetime` object for January 1, 2100
    2. This uses the `future` object to create a `Task` scheduled for January 1, 2100

=== ":three: TimeTrigger"

    These triggers are similar to DateTriggers, but trigger daily at the specified hour, minute, and second.

    ```python
    from interactions import Task, TimeTrigger

    @Task.create(TimeTrigger(hour=0, minute=0)) # (1)!
    async def midnight():
        print("It's midnight!")
    ```
    { .annotate }

    1. This creates a task to run at midnight every day

=== ":four: OrTrigger"

    These triggers are special, in that you can pass in a list of different triggers, and if any of them are triggered, it runs the function.

    ```python
    from interactions import Task, OrTrigger, TimeTrigger

    @Task.create(OrTrigger(TimeTrigger(hour=5, minute=0), TimeTrigger(hour=17, minute=0)) # (1)!
    async def five():
        print("It's 5 O'clock somewhere, and that somewhere is here!")
    ```
    { .annotate }

    1. This creates a task that triggers at either 5 AM local time or 5 PM local time

## Starting a task

To start a task that has been created, you need to run the `Task.start()` method from an `async` function. A good place to do this is during `on_startup`:
=== ":one: Decorators"

    ```python
    from interactions import Client, Intents, Task, IntervalTrigger, listen

    @Task.create(IntervalTrigger(minutes=10))
    async def print_every_ten():
        print("It's been 10 minutes!")

    bot = Client(intents=Intents.DEFAULT)

    @listen()
    async def on_startup(): # (1)!
        print_every_ten.start()
    ```
    { .annotate }

    1. See [Events](/interactions.py/Guides/10 Events/) for more information

=== ":two: Manual Registration"

    ```python
    from interactions import Client, Intents, Task, IntervalTrigger, listen

    async def print_every_ten():
        print("It's been 10 minutes!")

    bot = Client(intents=Intents.DEFAULT)
    task = Task(print_every_ten, IntervalTrigger(minutes=10))

    @listen()
    async def on_startup():
        task.start()
    ```


# Sharding

Oh damn, your bot is getting pretty big, huh? Well I guess its time we discuss sharding.

Sharding, in the simplest sense, is splitting up the load on your bot. Discord requires sharding once you reach 2500 guilds, but your bot might be able to handle more than that with a single process.
That's where the [AutoShardedClient](/interactions.py/API Reference/API Reference/AutoShardClient) comes in.

The AutoShardedClient is a subclass of the [Client](/interactions.py/API Reference/API Reference/Client) class, and it's basically the same as the Client class, except it's automatically sharding your bot under the hood.
Simply start your bot with this client, and it will automatically shard based on Discord's requests. If you need to, you can also manually specify shards.

How do you use it? Well that's the easy part, lets say this is your code

```python
from interactions import Client, listen

class Bot(Client):
    async def on_ready(self):
        print("Ready")
        print(f"This bot is owned by {self.owner}")

    @listen()
    async def on_message_create(self, event):
        print(f"message received: {event.message.content}")
```
To make it sharded we make one change:
```python
from interactions import AutoShardedClient, listen

class Bot(AutoShardedClient):
    async def on_ready(self):
        print("Ready")
        print(f"This bot is owned by {self.owner}")

    @listen()
    async def on_message_create(self, event):
        print(f"message received: {event.message.content}")
```
And that's it, your bot is now able to automatically shard.

Sounds pretty cool, huh? So what's the catch? Well, this keeps the bot in a single process, meaning there is no load-balancing.
If your bot is getting large, no matter how many shards you have, it will be slow. That's where splitting the bot into multiple processes is the best solution. But that's outside the scope of this guide 😉.


# Examples

## `main.py`

```python

import logging

from interactions import Client, Intents, listen
from interactions.api.events import Component
from interactions.ext import prefixed_commands

# define your own logger with custom logging settings
logging.basicConfig()
cls_log = logging.getLogger("MyLogger")
cls_log.setLevel(logging.DEBUG)

bot = Client(
    intents=Intents.DEFAULT | Intents.MESSAGE_CONTENT,
    sync_interactions=True,
    asyncio_debug=True,
    logger=cls_log
)
prefixed_commands.setup(bot)


@listen()
async def on_ready():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


@listen()
async def on_guild_create(event):
    print(f"guild created : {event.guild.name}")


# Message content is a privileged intent.
# Ensure you have message content enabled in the Developer Portal for this to work.
@listen()
async def on_message_create(event):
    print(f"message received: {event.message.content}")


@listen()
async def on_component(event: Component):
    ctx = event.ctx
    await ctx.edit_origin("test")


bot.load_extension("test_components")
bot.load_extension("test_application_commands")
bot.start("Token")
```

## `test_components.py`

```python

from interactions import Button, ActionRow, ButtonStyle, Extension
from interactions.ext.prefixed_commands import prefixed_command


class ButtonExampleSkin(Extension):
    @prefixed_command()
    async def blurple_button(self, ctx):
        await ctx.send("hello there", components=Button(ButtonStyle.BLURPLE, "A blurple button"))

    @prefixed_command()
    async def multiple_buttons(self, ctx):
        await ctx.send(
            "2 buttons in a row",
            components=[Button(ButtonStyle.BLURPLE, "A blurple button"), Button(ButtonStyle.RED, "A red button")],
        )

    @prefixed_command()
    async def action_rows(self, ctx):
        await ctx.send(
            "2 buttons in 2 rows, using nested lists",
            components=[[Button(ButtonStyle.BLURPLE, "A blurple button")], [Button(ButtonStyle.RED, "A red button")]],
        )

    @prefixed_command()
    async def action_rows_more(self, ctx):
        await ctx.send(
            "2 buttons in 2 rows, using explicit action_rows lists",
            components=[
                ActionRow(Button(ButtonStyle.BLURPLE, "A blurple button")),
                ActionRow(Button(ButtonStyle.RED, "A red button")),
            ],
        )


def setup(bot):
    ButtonExampleSkin(bot)
```

## `test_application_commands.py`

```python

from interactions import slash_command, slash_option, SlashContext, context_menu, CommandType, Button, ActionRow,
    ButtonStyle, Extension


class CommandsExampleSkin(Extension):
    @slash_command("command", description="This is a test", scopes=701347683591389185)
    @slash_option("another", "str option", 3, required=True)
    @slash_option("option", "int option", 4, required=True)
    async def command(self, ctx: SlashContext, **kwargs):
        await ctx.send(str(ctx.resolved))
        await ctx.send(f"Test: {kwargs}", components=[ActionRow(Button(1, "Test"))])
        print(ctx.resolved)

    @command.error
    async def command_error(self, e, *args, **kwargs):
        print(f"Command hit error with {args=}, {kwargs=}")

    @command.pre_run
    async def command_pre_run(self, context, *args, **kwargs):
        print("I ran before the command did!")

    @context_menu(name="user menu", context_type=CommandType.USER, scopes=701347683591389185)
    async def user_context(self, ctx):
        await ctx.send("Context menu:: user")


def setup(bot):
    CommandsExampleSkin(bot)
```


# Migrating from discord.py

1. interactions.py requires python 3.10 (as compared to dpy's 3.5), you may need to upgrade python.
     - If you see `ERROR: Could not find a version that satisfies the requirement discord-py-interactions (from versions: none)` when trying to `pip install discord-py-interactions`, this is your problem.

2. Classes/Models
     - Your client is `interactions.Client`.
     - Cogs are `Extensions`.
     - `Member` is not a subclass of `User`, if you're using `isinstance`, you'll want to check both explicitly.

3. Extensions (Cogs)
     - These work mostly the same, with a few notable changes:
     - Your setup function doesn't need to do `bot.add_cog()`.  Simply call `MyCog(bot)`, and it'll automatically register itself.
     - Extensions already define `self.bot`, you don't need to do that in your `__init__` function.
     - For a full example, see [here](/interactions.py/Guides/20 Extensions/)

4. Event handlers
     - Register event handlers with `@interactions.listen`
     - Where possible, we use the official names for events, most notably `on_message_create` instead of dpy's `on_message`.
       - A full list can be found [here](/interactions.py/API Reference/API Reference/events/discord/).
     - Event details are stored on a model, passed as a single parameter. (eg: `on_member_update(before, after)` becomes `on_member_update(event)`, where event has a `.before` and `.after`.
     - `on_ready` is called whenever the gateway resumes. If you are looking to run stuff *once* upon startup, use the `on_startup` handler instead.
     - For more details, read [the Events guide](/interactions.py/Guides/10 Events).

5. Migrating your commands
     - If you were already using dpy's command extension, migrating to slash commands is fairly simple.  You just need to convert the decorators as per the [Slash Commands guide](/interactions.py/Guides/03 Creating Commands/)
     - If you wish to keep using prefixed commands (sometimes called message or text-based commands), you can use our prefixed command extension, which has an [extensive guide for them](/interactions.py/Guides/07 Creating Prefixed Commands). The syntax should be very similar to discord.py with a few exceptions.
     - If you were manually handling commands with `on_message`, you'll probably need to figure it out yourself, as this guide doesn't know how you wrote your parser.  Consider using the provided command handlers.

???+ Note
    This guide was written based on the experiences of porting a small handful of bots.  There may be gotchas that we did not encounter.  If you run into anything you'd like to have known, let us know in our Discord, and we'll add it to this document.


# Migrating from 4.X

Version 5.X (and beyond) is a major rewrite of interactions.py compared to 4.X, though there have been major improvements to compensate for the change. 5.X was designed to be more stable and flexible, solving many of the bugs and UX issues 4.X had while also adding additional features you may like.

**You will need to do some updating and rewriting of your code,** but it's not as daunting as it may seem. We've provided this document as a starting point (*though it is not exhaustive*), and we have plenty of guides and documentation to help you learn the other parts of this library. Lastly, our support team is always here to help if you need it [in our Discord server](discord.gg/interactions).

Now, let's get started, shall we?

???+ note
    In v5's documentation, you will often see imports using the format `from interactions import X`, unlike v4. You can still use `import interactions` and do `interactions.X` though.

    Events, errors, and utilities are under their own sub-namespace when using `import interactions`. For example, events are under `interactions.events.X`.

## Python Version Change

Starting from version 5, **Python 3.10 or higher is now required**, whereas version 4 only needed 3.8+. This is because 5.x incorporates many new and exciting features introduced in more recent versions of Python.

For Windows users, this is usually as simple as downloading 3.10 or higher (ideally the latest version for the most speed and features) and possibly removing the old version if you have no other projects that depend on older versions.

For Linux and MacOS, we recommend using [pyenv](https://github.com/pyenv/pyenv); _pyenv lets you easily switch between multiple versions of Python. It's simple, unobtrusive, and follows the UNIX tradition of single-purpose tools that do one thing well._ We strongly suggest consulting pyenv's guides on installation.

If you prefer not to use pyenv, there are many guides available that can help you safely install a newer version of Python alongside your existing version.

## Slash Commands

Slash commands function differently from v4's commands - it's worth taking a good look at the guide to see [how they work in the library now](../03 Creating Commands).

Big changes include the fact that `@bot.command` (we'll get to extensions later) is now `@interactions.slash_command`, and `CommandContext` is now `SlashContext`. There may be some slight renamings elsewhere too in the decorators itself - it's suggested you look over the options for the new decorator and appropriately adapt your code.

Arguably the biggest change involves how v5 handles slash options. v5's primary method relies heavily on decorators to do the heavy lifting, though there are other methods you may prefer - again, consult the guide, as that will tell you every method. A general rule of thumb is that if you did not use the "define options as a list right in the slash command decorator" choice, you will have to make some changes to adjust to the new codebase.
Subcommands also cannot be defined as an option in a command. We encourage you to use a subcommand decorator instead, as seen in the guide.

If you were using some of the more complex features of slash commands in v4, it's important to note: *v5 only runs the subcommand, not the base-command-then-subcommands that you could do with v4.* This was mostly due to the logic being too complex to maintain - it is encouraged that you use checks to either add onto base commands or the subcommands you want to add them to, as will be talked about in an upcoming section. `StopIteration` also doesn't exist in v5 due to this change.

Autocomplete *is* different. v5 encourages you to tie autocompletes to specific commands in a different manner than v4 and uses a special context, [like seen in the guide](../03 Creating Commands/#i-need-more-than-25-choices). There is `interactions.global_autocomplete` too.

Autodeferring is also pretty similar, although there's more control, with options to allow for global autodefers and extension-wide ones.

## Events

Similarly to Slash Commands, events have also been reworked in v5. Instead of `@bot.event` and `@extension_listener`, the way to listen to events is now `@listen`. There are multiple ways to subscribe to events, whether it is using the function name or the argument of the `@listen` decorator. You can find more information on handling events using v5 [on its own guide page](../10 Events).

An important note: events now dispatch an event object that contains every part about an event, instead of the object that directly corresponds to an event. For example, message creation now looks like this:
```python
from interactions import listen
from interactions.api.events import MessageCreate

@listen()
async def on_message_create(event: MessageCreate):
    event.message  # actual message
```

This is more notable with events that used to have two or more arguments. They *also* now only have one event object:
```python
from interactions.api.events import MemberUpdate

@listen()
async def on_member_update(event: MemberUpdate):
    event.before  # before update
    event.after  # after update
```

## Other Types of Interactions (Context Menus, Components, Modals)

These should be a lot more familiar to you - many interactions in v5 that aren't slash commands are similar to v4, minus name changes (largely to the decorators and classes you use). They should still *function* similarly though, but it's never a bad idea to consult the various guides that are on the sidebar to gain a better picture of how they work.

[If you're using context menus](../04 Context Menus) (previously `@bot.user_command` or `@bot.message_command`), the decorators have changed to `@user_context_menu` and `@message_context_menu`, or you can also use the more general `@context_menu` decorator and specify the type of context menu through `context_type` - otherwise, it's mostly the same.

There also is no "one decorator for every type of command" - there is no equivalent to `bot.command`, and you will need to use the specialized decorators instead.

For example:
```python
@slash_command(...)  # for slash commands
@subcommand(...)  # for slash subcommands
@context_menu(...)  # for context menus
@component_callback(...)  # for component callbacks
@modal_callback(...)  # for modal callbacks
```

[For components](../05 Components) and [modals](../06 Modals): you no longer need to use `ActionRow.new(...)` to make an ActionRow now - you can just use `ActionRow(...)` directly. You also send modals via `ctx.send_modal` now. Finally, text inputs in components (the options for string select menus, and the components for modals) are also `*args` now, instead of being a typical parameter:
```python
import interactions

# in v4:

components = [interactions.TextInput(...), interactions.TextInput(...)]

modal = interactions.Modal(
    title="Application Form",
    custom_id="mod_app_form",
    components=components,
)

# in v5:

components = [interactions.InputText(...), interactions.InputText(...)]

modal = interactions.Modal(
    *components,
    title="Application Form",
    custom_id="mod_app_form",
)
```

Otherwise, beyond renamings, components are largely the same.

## Extensions (cogs)

Extensions have not been changed too much. `await teardown(...)` is now just `drop(...)` (note how drop is *not* async), and you use `bot.load_extension`/`bot.unload_extension` instead of `bot.load`/`bot.unload`.

There is one major difference though that isn't fully related to extensions themselves: *you use the same decorator for both commands/events in your main file and commands/events in extensions in v5.* Basically, instead of having `bot.command` and `interactions.extension_command`, you *just* have `interactions.slash_command` (and so on for context menus, events, etc.), which functions seemlessly in both contexts.

Also, you no longer require a `setup` function. They can still be used, but if you have no need for them other than just loading the extension, you can get rid of them if you want.

## Cache and interactions.get

Instead of the `await interactions.get` function in v4, v5 introduces the `await bot.fetch_X` and `bot.get_X` functions, where `X` will be the type of object that you would like to retrieve (user, guild, role...). You might ask, what is the difference between fetch and get?

The answer is simple, `get` will look for an object that has been cached, and therefore is a synchronous function that can return None if this object has never been cached before.

On the other hand, `fetch` is an asynchronous function that will request the Discord API to find that object if it has not been cached before. This will *fetch* the latest version of the object from Discord, provided that the IDs you inputted are valid.

## Library extensions

In v4, many extensions could be separately added to your bot to add external functionalities (molter, paginator, tasks, etc...). Many of those extensions were merged in the main library for v5, therefore you will NOT need to download additional packages for functionalities such as prefixed commands, pagination, tasks or sharding.

## asyncio Changes

In recent Python versions, `asyncio` has gone through a major change on how it treats its "loops," the major thing that controls asynchronous programming. Instead of allowing libraries to create and manage their own loops, `asyncio` now encourages (and soon will enforce) users to use one loop managed by `asyncio` itself.

What this means to you is that *the `Client` does not have a loop variable, and no `asyncio` loop exists until the bot is started (if you use `bot.start()`).*

For accessing the loop itself, there is [`asyncio.get_running_loop()`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.get_running_loop) to, well, get the running loop, though you're probably using the loop to run a task - it's better to use [`asyncio.create_task(...)`](https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task) for that instead if you are.

However, as for the second point... it shouldn't impact most users, but this may if you use `create_task` to run an asynchronous function before the bot starts - *this including loading in an extension that uses it before the bot is properly started.* Both of the above functions will error out if used, so using them isn't an option.

So what do you do? Simple - create the loop "yourself" and use `bot.astart()` instead!

Before:
```python
import interactions

# if there's no loop detected, v4 would create the loop for you at this point
# it also stores the loop in bot._loop
bot = interactions.Client(...)

bot._loop.create_task(some_func())
bot.load("an_ext_that_uses_the_event_loop")

bot.start()
```

After:
```python
import asyncio
import interactions

# no bot._loop, loop also does not exist yet
bot = interactions.Client(...)

async def main():
    # loop now exists, woo!
    asyncio.create_task(some_func())
    bot.load_extension("an_ext_that_uses_the_event_loop")
    await bot.astart()

# a function in asyncio that creates the loop for you and runs
# the function within
asyncio.run(main())
```

It's worth noting that you can continue to use `bot.start()` and not change your code if you never relied on `asyncio` like this.


# Migrating from NAFF

Oh hey! So you're migrating from NAFF to interactions.py? Well lets get you sorted.

First and foremost, you'll need to install the new library. You can do this by running `pip install interactions.py` in your terminal.
Then, the first thing you'll need to do is change your imports. You'll need to change `from naff import _` to `from interactions import _`. To be honest, assuming your code is relatively simple, you should be able to use find and replace to do this.

## Prefixed Commands
I.py moves prefixed commands to an extension, rather than being a part of the client. So to use them you'll need to load them.
```python
from interactions import Client, Intents
from interactions.ext import prefixed_commands

# guild messages are included in the default intents ipy uses
# if you wish for the prefix to be anything but mentioning the bot,
# guild message content will also be required
client = Client(..., intents=Intents.GUILD_MESSAGES | ...)
prefixed_commands.setup(client)
```
From here it's more or less the same as before. You can find a guide on how to use prefixed commands [here](/interactions.py/Guides/26 Prefixed Commands/).

## Hybrid Commands
For now, hybrid commands are not supported, but they will be in the future.

## Enums
To get us on the same page. Enums are a way of defining a set of constants. For a Discord example, ButtonStyles.
In v5, enums are no longer plural. So `ButtonStyles` is now `ButtonStyle`. This applies to all enums in the library.

## StringSelectMenu
`StringSelectMenu` now takes it's options as positional arguments, rather than a list. This means that you can no longer do `StringSelectMenu(options=[...])`, instead the quickest way to do it is `StringSelectMenu(*[...])`.
Alternatively, I recommend this syntax:
```python
StringSelectMenu(
    "Thing 1", "Thing 2", "Thing 3",
    placeholder="Pick a thing"
)
```
This is much more readable, and removes useless boilerplate.

## Modals
Much like `StringSelectMenu`, Modals now take their children as positional arguments, rather than a list. This means that you can no longer do `Modal(components=[...])`, instead the quickest way to do it is `Modal(*[...])`.
Again, the same recommendation applies here:
```python
Modal(
    ShortText(label="Short Input Text", custom_id="short_text"),
    ParagraphText(label="Long Input Text", custom_id="long_text"),
    title="My Modal",
)
```

## Kwargs Vs. Args
V5 prefers kwargs over args. This means for the majority of methods and objects, they expect their arguments to be passed as kwargs, rather than args. This is to make the library more readable, and to make it easier to add new arguments in the future.
The **only** exceptions to this are list-like objects, like `ActionRow`, `StringSelectMenu`, `Modal`, where the children are passed as args in order to keep the syntax clean.


Let's be honest; reading API documentation is a bit of a pain.
These guides are meant to help you get started with the library and offer a point of reference.

???+ note
    As with many Python libraries, you may use `import interactions` and do `interactions.X` for your objects. The documentation leads more towards using `from interactions import X`, however.

    Events, errors, and utilities are under their own sub-namespace when using `import interactions`. For example, events are under `interactions.events.X`.

<div class="grid cards" markdown>

-   [__:material-star-shooting: Getting Started__](01 Getting Started.md)

    ---

    Ready to get your Python on and create a Discord bot? This guide's got you covered with installation options and a basic bot code example.

-   [__:material-hammer-screwdriver: Creating Your Bot__](02 Creating Your Bot.md)

    ---

    Want to create your own bot but don't know where to start? This guide has you covered from bot-tom to top!

-   [__:material-slash-forward-box: Slash Commands__](03 Creating Commands.md)

    ---

    Slash commands are a cut above the rest - this guide will show you how to create your very own slash commands.

-   [__:material-menu-open: Context Menus__](04 Context Menus.md)

    ---

    Create menus that are so good, they'll have your users right-clicking for more.

-   [__:material-button-cursor: Components__](05 Components.md)

    ---

    While interactions are cool and all, they are still missing a vital component. Introducing components, aka Buttons, Selects, soon Text Input Fields

-   [__:material-dock-window: Modals__](06 Modals.md)

    ---

    Ready to pop-up your user interface game? This guide will show you how to create modals.

-   [__:material-account-convert: Converters__](08 Converters.md)

    ---

    If your bot is complex enough, you might find yourself wanting to use custom models in your commands. Converters are classes that allow you to do just that.

-   [__:material-chat-alert: Events__](10 Events.md)

    ---

    HEY! LISTEN! If you want to know more about events, you can check out this guide.

-   [__:material-cogs: Extensions__](20 Extensions.md)

    ---

    Damn, your code is getting pretty messy now, huh? Wouldn't it be nice if you could organise your commands and listeners into separate files?

-   [__:material-music: Voice Support__](23 Voice.md)

    ---

    So you want to start playing some 🎵tunes🎶 in voice channels? Well let's get that going for you.


-   [__:material-earth-plus: Localisation__](24 Localisation.md)

    ---

    So your bot has grown, and now you need to ~~localize~~ localise your bot. Well thank god we support localisation then, huh?

-   [__:material-text: Prefixed Commands__](26 Prefixed Commands.md)

    ---

    Going old-school with prefixed-commands? No problem. Let's get your message commands up and running.

-   [__:material-book-open-page-variant: Pagination__](30 Pagination.md)

    ---

    We've all hit that point where Discord won't let you send enough characters, at that point you can either flood the channel with multiple messages, or you can start paginating your messages.

-   [__:octicons-clock-24: Tasks__](40 Tasks.md)

    ---

    Tasks are background processes that can be used to asynchronously run code with a specified trigger.

-   [__:material-call-split: Sharding__](80 Sharding.md)

    ---

    Oh damn, your bot is getting pretty big, huh? Well I guess its time we discuss sharding.

-   [__:material-frequently-asked-questions: Migration from discord.py__](97 Migration From D.py.md)

    ---

    What's the difference between interactions.py and discord.py?

-   [__:material-package-up: Migration from v4__](98 Migration from 4.X.md)

    ---

    How do I migrate from interactions.py v4 to v5?

-   [__:material-package-up: Migration from NAFF__](99 2.x Migration_NAFF.md)

    ---

    How do I migrate from NAFF to i.py v5?

</div>


