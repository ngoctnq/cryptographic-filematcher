# cryptographic filematcher
_crypto & netsec final project_ &mdash;&mdash; _rpi fall '17_

## introduction_

Two people, each does one pass of running Python scripts and sending out things, input their respective filepaths to be matched, and the program shows what files they have in common.

## specifications_

This is an implementation based on the _Partially Homomorphic Encryption_ called **Paillier Encryption**.

The hashes are done with SHA3-512 just to be on the safe side.

## dependencies_

- Python 3.3 or above, which is the requirement for the `phe` module
- The <code>python-paillier</code> library, which gives the <code>phe</code> module
- GnuPG / OpenPGP, or literally trustworthy verification suite, for verification/authentication purposes

<sub>_Note 1:_ Installation of `python-paillier` on Ubuntu or such distros requires some more dependencies: `libmpc-dev`, `libmpfr-dev`, `libmpfr4`, `libgmp3-dev` for high-precision computations. <sup id="a1">[[1]](#f1)</sup></sub>

<sub>_Note 2:_ We assume that you already know how to sign and verify a file. At the very least, please publish your public key, and then follow this beginner-friendly guide. <sup id="a2">[[2]](#f2)</sup></sub>

## protocol_

<sup>_**Head note:** This protocol assumes that the public key of each party is public. If at any verification point does it fail to verify/autheticate, abort immediately. Also, all steps containing verification are not described in details, and thus we make up for that by the very emboldened font._</sup>

**Step 0:** get all the dependencies, publish both ends' public keys, (possibly toss a coin to) decide who gets to be the server first.

**Step 1:** the server runs `server_function.py` with the following syntax:

```sh
server_function.py [file_1] [file_2] ... [file_n]
```

where the files are the ones to be matched. This will export two files in destinations of your choice.

- The first one, **MUST BE KEPT SECRET**, is `KEY`, which holds your secret key for the Paillier encryption, and a dictionary of key-value pairs being your filepaths and their corresponding hashes.
- The second one, **MUST BE SIGNED WITH THE SERVER'S PRIVATE KEY AND SENT ALONG WITH THE MAC/SIGNATURE**, that will be sent to the client, is `COEFF`, which holds the public key ffor the Paillier encryption, and the encrypted coefficients of a polynomial with the server's files' hashes as roots.

**Step 2:** the client, after receiving `COEFF` and **CHECK THE VALIDITY OF THE FILE WITH THE SERVER'S PUBLIC KEY**, runs `client.py` with the following syntax:

```sh
client.py [file_1] [file_2] ... [file_n]
```

where the files are the ones to be matched. This will ask for the location of said `COEFF` file, and export a file `DIGEST` to be sent back to the server in a destination of your choice. This file contains the encrypted and randomized results of the evaluation of the server's function at the client's files' hashes. Similarly, **THIS MUST BE SIGNED WITH THE CLIENT'S PRIVATE KEY AND SENT ALONG WITH THE CORRESPONDING MAC/SIGNATURE**.

**Step 3**: the server, after receiving `DIGEST` and **CHECK THE VALIDITY OF THE FILE WITH THE CLIENT'S PUBLIC KEY**, runs `server_match.py` with no additional arguments. It will ask for the locations of the aforementioned files `KEY` and `DIGEST`, run some code execution, and tells the server what file(s) he/she has in common with the client.

**Step 4**: switch role, rinse and repeat back from step 1.

## security_

 We encrypt just about everything from the server/sender (S) end to hide all related information from S, then let the client/customer (C) do randomized arithmetics on it to get some encrypted result that is not public to C or the eavesdropper, while also not exposing any of C's information. This has been proven to be secure under the Semi-Honest model. <sup id="a3">[[3]](#f3)</sup>

 The hash function is state-of-the-art with the highest security possible. I opted for SHA-3/Keccak instead of SHA-2 because of all the wrong reasons, since SHA-3 is not supposed to be the successor of SHA-2, but rather an alternative if SHA-2 is ever broken. Still, SHA-3 is not yet broken either, so its use is justified.

 The hash comparisons are done using `compare_digest()` with no premature termination of loops to prevent side-channel attacks to the maximum.

 One weak point of this program is due to lack of peer-review in the imported `phe` module as the author acknowledged:

 > This code has neither been written nor vetted by any sort of crypto expert. The crypto parts are mercifully short, however. <sup id="a4">[[4]](#f4)</sup>

## improvements_

One simple way that would speed this up is to revert back to SHA-2 since it operates faster than SHA-3. Another way that is not really good is to decrease the security parameters of the involved security components (shorter hashes). The most important one is that this procedure is unnecessarily clunky; notably, the two sides have to run the procedure, with each once takes turn being the server/client. A better way to do this is a symmetric approach, as proposed by a few papers to date. <sup id="a5">[[5]](#f5)</sup>

## lessons_

I implemented a horrible version of this protocol before importing the `phe` module, so a lesson relearnt: *__never implement any crypto primitives by yourself__* - I believe I heard this from Dan Boneh in one of his lectures. I also started this the Tuesday night before the exam, so lesson *numer zwei*: *__start early. find teammates. plot out plans. do things the organized way. don't kill yourself over a possible bonus 10% in grade of class that is required for qual exam.__*

## citations_

<sup id="f1">[[1]](#a1)</sup> The documentation for the <code>phe</code> module can be found here: [python-paillier](http://python-paillier.readthedocs.io/en/latest/index.html).

<sup id="f2">[[2]](#a2)</sup> The GnuPG guide can be found here: [How to verify a PGP signature with GnuPG](http://www.mattnworb.com/post/how-to-verify-a-pgp-signature-with-gnupg/).

<sup id="f3">[[3]](#a3)</sup> The relevant paper describing the cryptomagic behind this can be found here: [Efficient Private Matching and Set Intersection](https://www.cs.princeton.edu/~mfreed/docs/FNP04-pm.pdf).

<sup id="f4">[[4]](#a4)</sup> The source code with the author's disclaimer can be found here: [python-paillier](https://github.com/n1analytics/python-paillier)

<sup id="f5">[[5]](#a5)</sup> The Cryptography StackExchange thread can be found here: [Is there an algorithm to find the number of intersections of two sets?](https://crypto.stackexchange.com/a/454).
