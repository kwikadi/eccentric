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
        self.mapping = [self.ec.mul(self.g, i) for i in range(self.eg.n)]
        if priv != -1:
            pub = self.eg.gen(priv,self.g)
            return_for_public = str(pub[0]) + " " + str(pub[1])
            return return_for_public
        else:
            return None


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
        for val, single in enumerate(cipher):
            if val == 0:
                enc_text.append(str(single[0][0]))
                enc_text.append(str(single[0][1]))
            enc_text.append(str(single[1][0]))
            enc_text.append(str(single[1][1]))

        return_val = " ".join(enc_text)
        return return_val

    def decryption(self, private_key, cipher_raw):
        cipher_raw_list = cipher_raw.split()
        cipher_super = []
        decrypted = []
        key = basicfunc.Coord(int(cipher_raw_list[0]), int(cipher_raw_list[1]))

        for i,k in zip(cipher_raw_list[2::2], cipher_raw_list[3::2]):
            cipher_super.append(basicfunc.Coord(int(i), int(k)))

        for cipher in cipher_super:
            decrypted.append(self.eg.dec((key,cipher), private_key, self.ec))

        final_dec = []
        for dec in decrypted:
            final_dec.append(unichr(self.mapping.index(dec)))

        return "".join(final_dec)
