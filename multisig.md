
# Python stellar-base multisig example

A document explaining how to do multisig
An example python file to test multisig... start with two addresses I created and funded these on testnet.

```These are on testnet already funded
public_keya = "GAY5DKIVAYZEESG6WVZCYPRFBN7O34U5U2CFZMGHX6MQEKJO5M57UYCQ"
private_keya = "SBFQV5S2EBUKW53UDYSYRSES4CR3CSR6TJV4BO34DPKKDKCSSTN7KQOV"

public_keyb = "GDXVAKMNRPF5LZOU4432OYHJO5JZD2V3UKI7PSPEGRAA7SG4VAFF5TT3"
private_keyb = "SDCGH6NN2ZD2LLKQDF5KMS2P7ZT7KGDDHZQRJGIWXMYGGNSCPCF5EVRN"
```


ensure you have pip install stellar-base already and launch python or ipython and have a look at the official docs first.

https://www.stellar.org/developers/guides/concepts/multi-sig.html
and the lab
https://www.stellar.org/laboratory/#txbuilder?params=eyJvcGVyYXRpb25zIjpbeyJpZCI6MCwiYXR0cmlidXRlcyI6e30sIm5hbWUiOiJzZXRPcHRpb25zIn1dfQ%3D%3D&network=test

```
from stellar_base.address import Address
from stellar_base.builder import Builder
b = Builder('SDCGH6NN2ZD2LLKQDF5KMS2P7ZT7KGDDHZQRJGIWXMYGGNSCPCF5EVRN')
b.append_set_options_op(master_weight=1,
                              med_threshold=1,
                              high_threshold=1,
                              signer_address='GAY5DKIVAYZEESG6WVZCYPRFBN7O34U5U2CFZMGHX6MQEKJO5M57UYCQ',
                              signer_type='ed25519PublicKey',
                              signer_weight=1,
                              source=None)
b.sign()
b.submit()
```

Ok you have setup the B address for multisig with threshold 1 for medium. Now try to send a transaction

```
b = Builder('SDCGH6NN2ZD2LLKQDF5KMS2P7ZT7KGDDHZQRJGIWXMYGGNSCPCF5EVRN')
b.append_payment_op('GAY5DKIVAYZEESG6WVZCYPRFBN7O34U5U2CFZMGHX6MQEKJO5M57UYCQ',1)
b.sign()
b.submit()
```

And sure enough it gets sent....

now change the threshold
```
b = Builder('SDCGH6NN2ZD2LLKQDF5KMS2P7ZT7KGDDHZQRJGIWXMYGGNSCPCF5EVRN')
b.append_set_options_op(master_weight=1,
                              med_threshold=2,
                              high_threshold=1,
                              signer_address='GAY5DKIVAYZEESG6WVZCYPRFBN7O34U5U2CFZMGHX6MQEKJO5M57UYCQ',
                              signer_type='ed25519PublicKey',
                              signer_weight=1,
                              source=None)
b.sign()
b.submit()
b = Builder('SDCGH6NN2ZD2LLKQDF5KMS2P7ZT7KGDDHZQRJGIWXMYGGNSCPCF5EVRN')
b.append_payment_op('GAY5DKIVAYZEESG6WVZCYPRFBN7O34U5U2CFZMGHX6MQEKJO5M57UYCQ',1)
b.sign()
b.submit()
```

And it should fail.... now send with 2 signatures

```

b = Builder('SDCGH6NN2ZD2LLKQDF5KMS2P7ZT7KGDDHZQRJGIWXMYGGNSCPCF5EVRN')
b.append_payment_op('GAY5DKIVAYZEESG6WVZCYPRFBN7O34U5U2CFZMGHX6MQEKJO5M57UYCQ',1)
b.sign(secret='SBFQV5S2EBUKW53UDYSYRSES4CR3CSR6TJV4BO34DPKKDKCSSTN7KQOV')
b.sign(secret='SDCGH6NN2ZD2LLKQDF5KMS2P7ZT7KGDDHZQRJGIWXMYGGNSCPCF5EVRN')
b.submit()

```
I explicitly signed with both and it should be sent....



