# [@typenullbot](https://twitter.com/typenullbot)

a robot that finds context-free error messages on stack overflow and posts them
to twitter

## setup

you'll need python 3

once you've cloned this repository and `cd`d into it, run:

```
pip3 install -r requirements.txt
```

(if that fails with a permissions error, perhaps you should try running it with
`sudo`)

that's it, you should now be able to run `python3 exception.py` and have it
show you error messages

## secret setup

the stack exchange API is throttled pretty heavily for unauthenticated users,
so you might want to provide api credentials (which you can read about [as part
of their api docs](http://api.stackexchange.com/docs/authentication)). make a
`secrets.py` file in the same directory as `exception.py` containing something
to the following effect:

```python
se_auth = {
    'client_id': 'your client id',
    'key': 'your key',
    'client_secret': 'your client secret',
    'access_token': 'an access token associated with your app',
}
```

`secrets.py` can also contain twitter API keys, but since all my robots handle
this in the same way, i'd rather document that centrally (i just haven't yet)
