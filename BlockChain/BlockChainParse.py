from Utils import *
import json

class BlockChainParse():
    magic_number = "f9beb4d9"
    btc_2_satoshi = 100000000

    def __init__(self):
        self._block_ = {
            "hash": "",
            "ver": 0,
            "prev_block": "",
            "mrkl_root": "",
            "time": 0,
            "bits": 0,
            "nonce": 0,
            "n_tx": 0,
            "size": 0,
            "tx": [],
            "mrkl_tree": [],
            "next_block": ""
        }

    '''
    def _tx_in_(self,hash, n, scriptSig):
        tx_in = {
            "prev_out": {
                "hash": hash,
                "n": n
            },
            "scriptSig": scriptSig
        }
        return tx_in

    def _tx_out_(self,value, scriptPubKey, address, hash=None, n=0):
        if (hash is None):
            tx_out = {
                "value": value,
                "scriptPubKey": scriptPubKey,
                "address": address
            }
        else:
            tx_out = {
                "value": value,
                "scriptPubKey": scriptPubKey,
                "address": address,
                "next_in": {
                    "hash": hash,
                    "n": n
                }
            }
        return tx_out

    def _tx_(self,hash, ver, vin_sz, vout_sz, lock_time, size, tx_in, tx_out, nid):
        tx = {
            "hash": hash,
            "ver": ver,
            "vin_sz": vin_sz,
            "vout_sz": vout_sz,
            "lock_time": lock_time,
            "size": size,
            "in": [].append(tx_in),
            "out": [].append(tx_out),
            "nid": nid
        }
        return tx
    '''

    def block_parse(self,block_data):
        index = 8
        block_size = block_data[index:index + 8]
        index += 8

        self._block_["size"] = hexstr2int(str_reverse_on_byte(block_size))

        #header
        self.header_parse(block_data[index:index + 160])
        index += 160

        #transaction_count
        varint = get_varint(block_data[index:])
        self._block_["n_tx"] = hexstr2int(varint[0])
        index += (2 + varint[1])

        #transaction
        res_tx = self.tx_parse(block_data[index:],self._block_["n_tx"])
        self._block_["tx"] = res_tx
        return self._block_

    def header_parse(self,header_data):
        self._block_["hash"] = double_sha256(header_data,'little')#小端编码格式，大端编码显示
        offset = 0
        self._block_["ver"] = hexstr2int(str_reverse_on_byte(header_data[offset:offset + 8]))#小端编码格式，大端编码显示
        offset += 8
        self._block_["prev_block"] = str_reverse_on_byte(header_data[offset:offset + 64])#小端编码格式，大端编码显示
        offset += 64
        self._block_["mrkl_root"] = str_reverse_on_byte(header_data[offset:offset + 64])#小端编码格式，大端编码显示
        offset += 64
        self._block_["time"] = hexstr2int(str_reverse_on_byte(header_data[offset:offset + 8]))#小端编码格式，大端编码显示
        offset += 8
        self._block_["bits"] = hexstr2int(str_reverse_on_byte(header_data[offset:offset + 8]))#小端编码格式，大端编码显示
        offset += 8
        self._block_["nonce"] = hexstr2int(str_reverse_on_byte(header_data[offset:offset + 8]))#小端编码格式，大端编码显示


    def tx_parse(self,tx_data,tx_count):
        tx = []
        preoffset = offset = 0
        for tx_index in range(0,tx_count):
            each_tx = {"hash":"","ver":0,"vin_sz":0,"vout_sz":0,"lock_time":0,"size":0,"in":[],"out":[],"nid":""}
            # version
            each_tx["ver"] = hexstr2int(str_reverse_on_byte(tx_data[offset:offset + 8]))#小端编码格式，大端编码显示
            offset += 8

            # tx_in_count
            varint = get_varint(tx_data[offset:])
            each_tx["vin_sz"] = hexstr2int(varint[0])
            offset += (2 + varint[1])

            # tx_in
            res_tx_in = self.tx_in_parse(tx_data[offset:], each_tx["vin_sz"])
            each_tx["in"] = res_tx_in[0]
            offset += res_tx_in[1]

            # tx_out_count
            varint = get_varint(tx_data[offset:])
            each_tx["vout_sz"] = hexstr2int(varint[0])
            offset += (2 + varint[1])

            # tx_out
            res_tx_out = self.tx_out_parse(tx_data[offset:],each_tx["vout_sz"])
            each_tx["out"] = res_tx_out[0]
            offset += res_tx_out[1]

            # lock_time
            each_tx["lock_time"] = hexstr2int(tx_data[offset:offset + 8])
            offset += 8

            #tx_hash
            each_tx["hash"] = double_sha256(tx_data[preoffset:offset],'little')#小端编码格式，大端编码显示
            self._block_["mrkl_tree"].append(each_tx["hash"])
            each_tx["size"] = int((offset - preoffset) / 2)
            preoffset = offset

            tx.append(each_tx)

        self._block_["mrkl_tree"] = get_merkle_tree(self._block_["mrkl_tree"])
        #print(tx)
        return tx

    def tx_in_parse(self,tx_in_data, tx_in_count):
        tx_in = []
        offset = 0
        for tx_in_index in range(0,tx_in_count):
            pre_out_hash =tx_in_data[offset:offset + 64]
            if(pre_out_hash ==  "0000000000000000000000000000000000000000000000000000000000000000"):
                each_tx_in = {"pre_out":{"hash":"","n":0},"coinbase_size":"","coinbase":"","sequence":0}
            else:
                each_tx_in = {"pre_out": {"hash": "", "n": 0}, "script_size": "", "scriptSig": "", "sequence": 0}

            # previous_out_hash
            each_tx_in["pre_out"]["hash"] = str_reverse_on_byte(pre_out_hash)#小端编码格式，大端编码显示
            offset += 64

            # previous_out_index
            each_tx_in["pre_out"]["n"] = hexstr2int(str_reverse_on_byte(tx_in_data[offset:offset + 8]))#小端编码格式，大端编码显示
            offset += 8

            # script_size
            varint = get_varint(tx_in_data[offset:])
            if (pre_out_hash == "0000000000000000000000000000000000000000000000000000000000000000"):
                each_tx_in["coinbase_size"] = varint[0]
            else:
                each_tx_in["script_size"] = varint[0]
            int_script_size = hexstr2int(varint[0])
            offset += (2 + varint[1])

            # signature_script
            if (pre_out_hash == "0000000000000000000000000000000000000000000000000000000000000000"):
                each_tx_in["coinbase"] = tx_in_data[offset:offset + int_script_size * 2]
            else:
                each_tx_in["scriptSig"] = tx_in_data[offset:offset + int_script_size * 2]
            offset += int_script_size * 2

            # sequence
            each_tx_in["sequence"] = hexstr2int(str_reverse_on_byte(tx_in_data[offset:offset + 8]))#小端编码格式，大端编码显示
            offset += 8

            tx_in.append(each_tx_in)

        #print(tx_in)
        return tx_in,offset

    def tx_out_parse(self,tx_out_data,tx_out_count):
        tx_out = []
        offset = 0
        for tx_out_index in range(0,tx_out_count):
            each_tx_out = {"value":0,"pk_script_size":"","pk_script":"","address":""}
            # value
            each_tx_out["value"] = hexstr2int(str_reverse_on_byte(tx_out_data[offset:offset + 16])) / self.btc_2_satoshi#小端编码格式，大端编码显示
            offset += 16

            # pk_script_size
            varint = get_varint(tx_out_data[offset:])
            each_tx_out["pk_script_size"] = varint[0]
            int_pk_script_size = hexstr2int(varint[0])
            offset += (2 + varint[1])

            # pk_script
            each_tx_out["pk_script"] = tx_out_data[offset:offset + int_pk_script_size * 2]
            offset += int_pk_script_size * 2

            tx_out.append(each_tx_out)

        #print(tx_out)
        return tx_out,offset


if(__name__ == '__main__'):
    bcp = BlockChainParse()
    res = bcp.tx_parse("01000000018dd4f5fbd5e980fc02f35c6ce145935b11e284605bf599a13c6d415db55d07a1000000008b4830450221009908144ca6539e09512b9295c8a27050d478fbb96f8addbc3d075544dc41328702201aa528be2b907d316d2da068dd9eb1e23243d97e444d59290d2fddf25269ee0e0141042e930f39ba62c6534ee98ed20ca98959d34aa9e057cda01cfd422c6bab3667b76426529382c23f42b9b08d7832d4fee1d6b437a8526e59667ce9c4e9dcebcabbffffffff0200719a81860000001976a914df1bd49a6c9e34dfa8631f2c54cf39986027501b88ac009f0a5362000000434104cd5e9726e6afeae357b1806be25a4c3d3811775835d235417ea746b7db9eeab33cf01674b944c64561ce3388fa1abd0fa88b06c44ce81e2234aa70fe578d455dac00000000",1)
    print(json.dumps(res))
