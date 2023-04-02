# Light ChatGPT (Client)

*Light ChatGPT is a light-weight application for ChatGPT. The client is buit with Python and PyQT5.* 

****
### Requirements

Python 3.8 and packages in `envs/requirements.txt` are recommanded.

****
### Usage

You can choose to run the application in python or in .exe file freely :

**1. Run the GUI with python**:

```bash
python light_chat.py
```

**2. Install and run .exe application**:

```bash
python install.py
```

Then the application is installed in folder `./dist/light_chat`, and the application file is in  `./dist/light_chat/light_chat.exe`.

****
### Manual

*Light Chat* consists of a main application and optional plugins. By default we provide two plugins : *light chat* and *google translation*.

#### 1. The main application

<details>

<summary> It consists of Floating window, Main window and Tray icon. </summary>

- Floating window:
  - `left-click`[`hot-key:ctrl+t`] - show the main window
  - `right-click` - show a menu
    - `user` - set user information
    - `to tray` - shrink to the tray icon
    - `close` - close the applciation 
- Main window:
  - `title` - is on the top of the window
    - `plugin name` - shows the name of current plugin, e.g., `light chat` 
      - switch the plugin by *moving your mouse on it and click the target plugin*.
      - [`hot-key:ctrl+tab`] : swtich to the next plugin
    - `shrink icon`[`hot-key:ctrl+t`] - shrink the window into the floating window
  - `plugin` - the main content of the window, e.g., `Light Chat` plugin.
  - [`hot-key:ctrl+q`] : close the application
- Tray icon:
  - `right-click` - show a menu
    - `show / hide` - show / hide the application
    - `close` - close the applciation 

</details>


#### 2. Plugin : Light Chat


<details>

<summary> A light plugin for OpenAI ChatGPT </summary>

- Display region - show the history questions / answers
  - `questions` - shown with white background
  - `answers` - shown with gray background
- Control region - get input from you
  - `send icon`[`hot-key:enter`] - send the text in the text box
  - `text box` - input your question in it
  - `new icon`[`hot-key:ctrl+n`]- refresh the history and start a new chat

</details>


#### 3. Plugin : Google Translation


<details>

<summary> A plugin for Google translation web server </summary>

- Display region - show the history translation items
  - `text` - shown with white background
  - `result` - shown with gray background
- Control region - get input from you
  - `send icon`[`hot-key:enter`] - send the text in the text box
  - `text box` - input your question in it
  - `new icon`[`hot-key:ctrl+n`]- refresh the history

</details>


****
### Add your own plugin

<details>

<summary> You can program your own plugin and add it to the application </summary>

1. Program a plugin file (we provide a template in `GUI/plugins/template.py`)
2. Put it in `GUI/plugins/`
3. Change the loaded plugins in `GUI/client.py` : 
    ```
    # this command is in LightChatGPTClient.__init__ : 
    self.main_window = MainWindow([..., "your_plugin_file_name"], self)
    ```
4. Run the application

</details>

****
### TODOs
- [x] Plugin - ChatGPT
- [x] Plugin - Google translation 
- [ ] Plugin - AI drawing
- [ ] GUI - relative size adjustment
- [ ] GUI - resize window

****
> Contact us:
> - jzy_ustc@mail.ustc.edu.cn
> - bitaswood@mail.ustc.edu.cn