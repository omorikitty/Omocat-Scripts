# Intallation

Put the Following Commands on your Linux Machine or your Cloud Host to Install the Server Requirements and it Works

## Requirements
```bash
sudo apt -y update

sudo apt install -y python python2.7 libsdl2-2.0.0 libpython2.7 python-pip git && \
python -m pip install requests "pymongo[srv]==3.3" beautifulsoup4

git clone https://github.com/omorikitty/Omocat-Scripts.git

cd Omocat-Scripts

chmod 755 bombsquad_server bs_headless
```

## Run Server
```bash
tmux new -s [name your session]
./bombsquad_server
```

# MongoDB Atlas Connection

This guide will help you create a free MongoDB Atlas account, set up a cluster, and connect to the database

## Step 1: Create a Free MongoDB Atlas Account

1. **Visit the MongoDB Atlas Website:**
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register).

2. **Sign Up:**
   - Fill in the registration form with your email, name, and a password. You can also sign up using your Google or GitHub account.

3. **Deploy your Cluster:**
   - Select the free cluster type M0.
   - After signing up and verifying your account. Select a region close to your location to reduce latency.
   - Create Deployment

4. **Create a Database User:**
   - Create a user with a username and password that you will use to connect to the database.
   - Create a Database User
  
5. **Choose Conection Method:**
   - Select the Drivers Option and then Choose Python Driver with Version 3.3 or Earlier

8. **Get the Connection String:**
   - Copy the provided connection string. It will look something like this:
     ```
     mongodb+srv://<username>:<password>@cluster0.mongodb.net/test?retryWrites=true&w=majority
     ```
     
7. **Configure IP Whitelist:**
   - Go to the "Network Access" tab and click on "Add IP Address".
   - Add your current IP address or allow access from any IP address (0.0.0.0/0) if you are working from different networks (not recommended for production).

## Step 2: Connect to MongoDB

Here is an example of how to connect to your MongoDB database:

1. **Connection Script:**
   - Go to (`DB_Manager.py`) and add your connection string, it should look something like this:

     ```python
     # Replace <username>, <password>, and <cluster-url> with your credentials and cluster URL
     client = pymongo.MongoClient('mongodb+srv://<username>:<password>@cluster0.mongodb.net/test?retryWrites=true&w=majority')
     ```
