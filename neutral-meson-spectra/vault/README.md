# Vault

This part of the repo should contain everything that is connected to data
flow and integrity.


It's important to establis stable connections with lxplus services in order to synchronize the data. Therefore authentification configuration should be described here


## Lxplus authentification
In order to login on lxplus machine do the following. Add the following configurations to your local `~/.ssh/config` as described [here](http://information-technology.web.cern.ch/services/fe/mac-support/howto/configure-ssh-password-less-login-lxplus-or-other-linux-boxen)

```
# file ~/.ssh/config
Host lxplus*.cern.ch
	GSSAPIAuthentication yes
	GSSAPIDelegateCredentials yes
```


Now to obtain the valid token one should do
```bash
kinit <CERN USER NAME>@CERN.CH
```
Please, note that the domain should be "CERN.CH" and **not** "LXPLUS.CERN.CH". And you can try logging in without typing a password:
```bash
ssh <CERN USER NAME>@lxplus.cern.ch
```

More information can be found on "official" [twiki](https://twiki.cern.ch/twiki/bin/view/LinuxSupport/SSHatCERNFAQ).

## Additional resources
List of interesting configurations/readings found while googling the the issues with kerberos:

- sshfs, kerberos with lxplus [pdf](https://rc.coepp.org.au/_media/presentations/20150324-sshfskerberos.pdf)
- useful shortcuts for authentification in a [blog](https://eothred.wordpress.com/2011/05/09/cern-and-kerberos-tokens/) post
- a [gist](https://gist.github.com/KFubuki/10728230) with configurations for ubuntu