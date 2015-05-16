import elliptic
import elgamal
import basicfunc

class Values():
    def public_key(self, a, b, q, priv):
        self.ec = elliptic.EC(a, b, q)
        for i in range(1, q):
            self.g, _ = self.ec.at(i)
            if self.g is not False and self.ec.order(self.g) <= self.ec.q and self.ec.order(self.g) > 127:
                break
        self.eg = elgamal.ElGamal(self.ec, self.g)
        pub = self.eg.gen(priv,self.g)
        return_for_public = str(pub[0]) + " " + str(pub[1])
        self.mapping = [self.ec.mul(self.g, i) for i in range(self.eg.n)]
        return return_for_public

    def encryption(self, pub_raw, message):
        pub1_list = pub_raw.split()
        pub1 = int(pub1_list[0])
        pub2 = int(pub1_list[1])
        publ = basicfunc.Coord(pub1,pub2)

        mapped = []
        for char in message:
            mapped.append(self.mapping[ord(str(char))])

        cipher = []
        for plain in mapped:
            cipher.append(self.eg.enc(plain, publ, self.g, 15))

        enc_text = []
        for single in cipher:
            enc_text.append(str(single[0][0]))
            enc_text.append(str(single[0][1]))
            enc_text.append(str(single[1][0]))
            enc_text.append(str(single[1][1]))

        return_val = " ".join(enc_text)
        return return_val

    def decryption(self, private_key, cipher_raw):
        cipher_raw_list = cipher_raw.split()
        cipher_super = []
        cipher_final = []
        decrypted = []
        
        for i,k in zip(cipher_raw_list[0::2], cipher_raw_list[1::2]):
            cipher_super.append(basicfunc.Coord(int(i), int(k)))

        for i,k in zip(cipher_super[0::2], cipher_super[1::2]):
            cipher_final.append((i,k))

        for ciphers in cipher_final:
            decrypted.append(self.eg.dec(ciphers, private_key, self.ec))

        final_dec = []
        for dec in decrypted:
            final_dec.append(unichr(self.mapping.index(dec)))

        return "".join(final_dec)

