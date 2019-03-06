# Extended baserequest importer

This python script is part of a larger toolset which allows importing a big list of urls together with all its found 
parameters using POST and GET through the Burp Suite Proxy.

## Why do you need this?

Often an attacker can find vulnerabilities in parameters which are obviously used within a page. But extracting this data
manually is a tidious work - wouldn't it be nice to have this process automated. That way you could send the found post
and get paramters to Burp Suite's active scanner and let it do the rest of the work.

## Execution

Plain and simple - it does not expect any arguments:

```
python3 extended-baserequest-importer.py
```

Don't forget to start Burp Suite Pro!

## How does this tool work?

__Example:__ https://brutelogic.com.br/xss.php

This site is well known and contains several xss. But sending this site to your active scanner will result in... nothing! 
The reason is: Burp doesn't know about a, b1, b2, b3, b4, c1, c2, c3, c4, c5 and c6. Maybe there are even more vulns to test
this parameters againat. Tunneling the following requests through 127.0.0.1:8080 (default Burp settings) will make them 
accessible in burp.

### Prepare your tool

You should rename the __example.app-settings.conf__ to app.settings.conf. Then adjust the settings. Usually the default 
ones are pretty good. But there are targets where sending 10 parameters per request is "healthier"!

### Step 1: Crawl the website

Using an initial request the html source code is extracted by this tool.


```
GET /xss.php HTTP/1.1
Accept-Encoding: gzip, deflate
Host: brutelogic.com.br
Content-Type: text/html
Accept: */*
User-Agent: Mozilla/5.0 (X11; Linux i586; rv:63.0) Gecko/20100101 Firefox/63.0
Referer: https://brutelogic.com.br/xss.php
Connection: close
```

### Step 2: Extract potentially useful parameters

I am bad at regular expression but my own work... you can take a look at inc/Parameters.py - using that regexpressions
this tool will extract the following parameters: b2, b3, b4, c1, c2, c3, c4, c5 and c6

### Step 3: Request the URL using GET/POST with those parameters

Now the tool just takes every parameters, appends a random string and requests the url again. When a lot parameters were 
extracted by this tool, the parameter list gets splitted in chunks with the same size. Its not good to send a GET request 
with 300 parameters + values. But usually you will have two requests per URL (POST and GET). They look like this:

#### The GET request:

```
GET /xss.php?0=393de39&1=e4390e4&12=7459b74&6=f9eb2f9&7=c3871c3&Find=46c5146&POST=dbfb5db&b1=cc50acc&b2=697b869&
b3=b5a91b5&b4=3b2083b&c1=4173e41&c2=2092f20&c3=242f424&c4=bdbc4bd&c5=32a8d32&c6=575e557&cloudflare=424fd42&
com=6f9f26f&googleapis=b695cb6&i=34e9034&js=5690156&min=789f378&php=d0b5ad0&submit=4298242&text=a238ca2&
viewport=92bb392 HTTP/1.1
Accept-Encoding: gzip, deflate
Host: brutelogic.com.br
Content-Type: text/html
Accept: */*
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36
Referer: https://brutelogic.com.br/xss.php
Connection: close
```

#### The POST request:

```
POST /xss.php HTTP/1.1
Accept-Encoding: gzip, deflate
Content-Length: 326
Host: brutelogic.com.br
Content-Type: application/x-www-form-urlencoded
Accept: */*
User-Agent: Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0
Referer: https://brutelogic.com.br/xss.php
Connection: close

0=393de39&1=e4390e4&12=7459b74&6=f9eb2f9&7=c3871c3&Find=46c5146&POST=dbfb5db&b1=cc50acc&b2=697b869&b3=b5a91b5&
b4=3b2083b&c1=4173e41&c2=2092f20&c3=242f424&c4=bdbc4bd&c5=32a8d32&c6=575e557&cloudflare=424fd42&com=6f9f26f&
googleapis=b695cb6&i=34e9034&js=5690156&min=789f378&php=d0b5ad0&submit=4298242&text=a238ca2&viewport=92bb392
```

As you can see not only the mentioned parameters were extracted, also some more are used here. Not perfect, but it's more
than enough!

### Step 4: Scan using Burp

By now you have those requests in your sitemap:

![sitemap](https://i.imgur.com/qBAWRlH.png)

You can now just start you scanner on those parameters and wait for something cool to happen ;=)

![intruder](https://i.imgur.com/B14o6lK.png)

