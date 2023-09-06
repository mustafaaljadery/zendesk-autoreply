# Auto respond to Tickets demo

The Zendesk app allows you to auto respond to support tickets. I scraped the entire Beehiiv knowledge-base and created a chat app that will automatically respond to zendesk support tickets. 

Here is a [demo]() of the app.

## Server

The server is built in python. It allows allows you to generate embeddings, store them in a vector DB, and query the OpenAI chat api. 

### Usage
```bash
pip install requirements.txt
```

Get the desired data in the data folder

**upload data**
```bash
py upload-data.py
```

**Run the flask server**
```bash
py main.py
```

## Zendesk App

### Usage
```bash
npx @zendesk/zcli apps:server
```

Navigate to your support ticket and add `?zcli_apps=true` to the end of the url.
