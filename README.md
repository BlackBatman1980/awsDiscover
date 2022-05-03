# awsDiscover
Enumerate AWS Assets

# Example Usage
python3 main.py example https

# Example Output
``` 
user@shell~$ python3 main.py example https
[*] Scanning: https://example-assets.s3.amazonaws.com
[+] 200 -- OK
[*] Enumerating https://example-assets.s3.amazonaws.com

Storage Class: STANDARD
ETag: "2efab932913158f7c075cf9b58740676"
Key: alitaPoster.jpg
Last Modified: 2019-03-28T17:07:53.000Z
Size: 80705


Storage Class: STANDARD
ETag: "a4f010401a23da159ef604ea9247ea13"
Key: _snapshot/test
Last Modified: 2022-03-15T15:39:51.000Z
Size: 107


Storage Class: STANDARD
ETag: "430496fa891378640caea0ce79c39c66"
Key: _snapshot/test2
Last Modified: 2022-03-15T15:39:58.000Z
Size: 125
```

