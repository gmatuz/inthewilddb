# Use the verified, up-to-date data of [inthewild.io](inthewild.io) directly
inTheWild is a community driven database and platform to help your vulnerability triage
## Who? How?
Information here can be useful for you if you are 
- In ops or vulnerability management and you want to know when to panic: sign up to RSS feed and add it to you notification list (e.g. Slack channel)
- Developing vulnerability management tool/service or enriching the output of one: download the database and write your wrapper or reuse ours if you python
- Triaging vulnerabilities or in a pentest looking for exploits: visit the site (e.g. [https://inthewild.io/vuln/CVE-2021-30666](https://inthewild.io/vuln/CVE-2021-30666) or use our always fresh [docker image](https://hub.docker.com/r/inthewild/inthewild/tags?page=1&ordering=last_updated) to get individual reports
## How to use the CLI
We provided a minimalistic CLI tool with the database to work as an example and if you want to script things without hammering our API :heart:
### How to install
It is not the 90s grandpa, stop installing utils writen by 2 randos! Use docker
### Getting reports
- You can get all exploits and exploitation reports related to vulnerability with its description in a nice table: `docker run inthewild/inthewild reports CVE-2021-30666`
- You can get just the exploits: `docker run inthewild/inthewild exploits CVE-2021-22986`
- Or just reports of exploitation in the wild: `docker run inthewild/inthewild exploitation CVE-2021-30666`
- _hey man, your table is dope but I heard JSON is cooler!_: `docker run inthewild/inthewild reports CVE-2021-30666 --no-format-cli`
- _this is confusing_: you may always add `--help` if you are getting lost
## How can I help out?
- Contribute with reports of exploitation inTheWild or exploits you misss
- Help triage said reports
- Send PR for your usecase
- Buy us a coffee