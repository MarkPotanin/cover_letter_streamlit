# Cover Letter Streamlit Application

The Cover Letter Writer helps you write a unique cover letter for each job application. You can try it on: `http://coverletter-writer.com/`.
If you have any questions, feel free to ask me at `tg:@zloypilgrim` or `mark.potanin@phystech.edu`.

Also [here](https://github.com/MarkPotanin/cover_letter_bot) is the repository with `Cover Letter Telegram Bot`. 

# Repository

This repository contains a simple streamlit application.

### 1. Get OpenAI API token.

* Go to `https://platform.openai.com/`
* Then go to `https://platform.openai.com/account/api-keys`,  or click the `View API keys` button in the upper right corner.
* reate a new key by clicking the `Create new secret key` button.
* Then use this API key inside `main.py` in the variable `openai.api_key` on line 16.

### 2. Cloud Server.

After obtaining OpenAI API key, you can run your application **locally** with `streamlit run main.py`. For production purposes, it's better to place the bot on a cloud server. I used `http://linode.com` (which offers a $100 trial period).

### 3. Service.

Run your application in the background on your cloud server. You can use my service file `cover_streamlit.service`.

* Place it in `/etc/systemd/system/cover_streamlit.service`.
* Don't forget to change: `User`, `WorkingDirectory` (path to cloned repo), and `ExecStart` (path to `main.py`). 
* Run your service with `systemctl start streamlit_app.service`. 

If you encounter any problems, read any tutorial about services (like [this](https://medium.com/codex/setup-a-python-script-as-a-service-through-systemctl-systemd-f0cc55a42267)). 

### 4. Domain.

I bought a domain for my streamlit application at `https://www.godaddy.com/`. It costs about 1$. I also place simple nginx config at `coverletter-writer.com` (should be place in `/etc/nginx/sites-available/coverletter-writer.com`).