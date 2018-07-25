
# Python stellar-base multisig example

A document explaining how to do multisig
An example python file to test multisig... start with two addresses I created and funded these on testnet.

```These are on testnet already funded
pub_keya = "GAY5DKIVAYZEESG6WVZCYPRFBN7O34U5U2CFZMGHX6MQEKJO5M57UYCQ"
pri_keya = "SBFQV5S2EBUKW53UDYSYRSES4CR3CSR6TJV4BO34DPKKDKCSSTN7KQOV"

pub_keyb = "GDXVAKMNRPF5LZOU4432OYHJO5JZD2V3UKI7PSPEGRAA7SG4VAFF5TT3"
pri_keyb = "SDCGH6NN2ZD2LLKQDF5KMS2P7ZT7KGDDHZQRJGIWXMYGGNSCPCF5EVRN"
```


ensure you have pip install stellar-base already and launch python or ipython and have a look at the official docs first.

https://www.stellar.org/developers/guides/concepts/multi-sig.html

and the lab
https://www.stellar.org/laboratory/#txbuilder?params=eyJvcGVyYXRpb25zIjpbeyJpZCI6MCwiYXR0cmlidXRlcyI6e30sIm5hbWUiOiJzZXRPcHRpb25zIn1dfQ%3D%3D&network=test


https://steemit.com/stellar/@mrbot/stellar-multi-sig-wallet-setup
```
from stellar_base.address import Address
from stellar_base.builder import Builder
b = Builder(pri_keyb)
b.append_set_options_op(master_weight=1,
                              med_threshold=1,
                              high_threshold=1,
                              signer_address=pub_keya,
                              signer_type='ed25519PublicKey',
                              signer_weight=1,
                              source=None)
b.sign()
b.submit()
```

Ok you have setup the B address for multisig with threshold 1 for medium. Now try to send a transaction

```
b = Builder(pri_keyb)
b.append_payment_op(pub_keya,1)
b.sign()
b.submit()
```

And sure enough it gets sent....

now change the threshold
```
b = Builder(pri_keyb)
b.append_set_options_op(master_weight=1,
                              med_threshold=2,
                              high_threshold=1,
                              signer_address=pub_keya,
                              signer_type='ed25519PublicKey',
                              signer_weight=1,
                              source=None)
b.sign()
b.submit()
b = Builder(pri_keyb)
b.append_payment_op(pub_keya,1)
b.sign()
b.submit()
```

And it should fail.... now send with 2 signatures

```

b = Builder(pri_keyb)
b.append_payment_op(pub_keya,1)
b.sign(secret=pri_keya)
b.sign(secret=pri_keyb)
b.submit()

```
I explicitly signed with both and it should be sent....


Finally if you want to use 2 servers and send for the signing...

```
c = Builder(pri_keyb)
c.append_payment_op(pub_keya,1)
data = c.gen_xdr()
# send text in data to other server

b = Builder(pri_keya)
b.import_from_xdr(data)
b.sign(pri_keya)
e = b.gen_xdr()

# send text in 'e' back to other server
c = Builder(pri_keyb)
c.import_from_xdr(e)
c.sign()
c.submit()
```






