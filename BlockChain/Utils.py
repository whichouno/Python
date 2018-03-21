import binascii
import base58
import hashlib
from hashlib import sha256
from ecdsa import SECP256k1,VerifyingKey,util,BadSignatureError
from six import b

#字符串按字节反转。大小端数据的字符串转换。eg:"123456" to "563412"
def str_reverse_on_byte(data):
    return binascii.hexlify(binascii.unhexlify(data)[::-1]).decode()

#16进制字符串转整型。eg:"11d" to 285
def hexstr2int(hexstr,byteorder='big'):
    return int.from_bytes(binascii.a2b_hex(hexstr), byteorder=byteorder)

###########################################################################################################
# get_varint(data):
#     解析varint
# params:
#     data:待解析数据。数据类型为:str
# return:
#     返回解析结果。数据类型为:tuple,长度为2。
#     tuple[0]为varint的数值位(不包含标识位),tuple[1]为数据位长度。数值位为小端存储。
###########################################################################################################
def get_varint(data):
    flag = hexstr2int(data[0:2])
    if flag < 253:
        return data[0:2],0
    if flag == 253:
        varint_size = 4
    elif flag == 254:
        varint_size = 8
    elif flag == 255:
        varint_size = 16
    return str_reverse_on_byte(data[2:varint_size + 2]),varint_size

###########################################################################################################
# single_sha256(data,byteorder = 'big'):
#     计算sha256
# params:
#     data:待计算数据。数据类型为:str
#     byteorder:字节序。"big"为大端,"little":为小端。数据类型为:str
# return:
#     返回sha256分散结果，数据类型为:str
###########################################################################################################
def single_sha256(data,byteorder = 'big'):
    if(byteorder == 'little'):
        res = binascii.hexlify(sha256(binascii.unhexlify(data)).digest()[::-1])
    else:
        res = binascii.hexlify(sha256(binascii.unhexlify(data)).digest())
    return res.decode()

###########################################################################################################
# double_sha256(data,byteorder = 'big'):
#     计算两次sha256
# params:
#     data:待计算数据。数据类型为:str
#     byteorder:字节序。"big"为大端,"little":为小端。数据类型为:str
# return:
#     返回两次sha256分散结果，数据类型为:str
###########################################################################################################
def double_sha256(data,byteorder = 'big'):
    if(byteorder == 'little'):
        res = binascii.hexlify(sha256(sha256(binascii.unhexlify(data)).digest()).digest()[::-1])
    else:
        res = binascii.hexlify(sha256(sha256(binascii.unhexlify(data)).digest()).digest())
    return res.decode()

###########################################################################################################
# single_ripemd160(data,byteorder = 'big'):
#     计算ripemd160
# params:
#     data:待计算数据。数据类型为:str
#     byteorder:字节序。"big"为大端,"little":为小端。数据类型为:str
# return:
#     返回ripemd160分散结果，数据类型为:str
###########################################################################################################
def single_ripemd160(data,byteorder = 'big'):
    if (byteorder == 'little'):
        res = binascii.hexlify(hashlib.new('ripemd160', binascii.unhexlify(data)).digest()[::-1])
    else:
        res = hashlib.new('ripemd160', binascii.unhexlify(data)).hexdigest()
    return res

###########################################################################################################
# single_base58(data):
#     base58编码
# params:
#     data:待做编码的数据。数据类型为:str
# return:
#     返回base58编码数据。数据类型为:str
###########################################################################################################
def single_base58(data):
    return base58.b58encode(binascii.unhexlify(data))

###########################################################################################################
# pubkey_2_btc_addr(pubkey,ver):
#     通过公钥计算比特币地址
# params:
#     pubkey:公钥,DER格式。数据类型为:str
#     ver:版本号,通常为"00"。数据类型为:str
# return:
#     返回比特币地址，数据类型为:str
###########################################################################################################
def pubkey_2_btc_addr(pubkey,ver):
    # 对pubKey计算sha256,结果再做ripemd160
    res_hash160 = single_ripemd160(single_sha256(pubkey))

    # 填充版本号,一般为00
    res_hash160 = ver + res_hash160

    # 计算两次sha256,所得结果的前8位作为校验值,填充到加密数据后
    res_dhash = double_sha256(res_hash160)
    res_dhash = res_hash160 + res_dhash[:8]

    # base58编码
    res_b58 = single_base58(res_dhash)
    return res_b58

###########################################################################################################
# pkhash_2_btc_addr(pkhash,ver):
#     通过公钥哈希值计算比特币地址
# params:
#     pkhash:公钥哈希值,即公钥计算SHA256和RIPEMD160后的值。数据类型为:str
#     ver:版本号,通常为"00"。数据类型为:str
# return:
#     返回比特币地址，数据类型为:str
###########################################################################################################
def pkhash_2_btc_addr(pkhash,ver):
    # 填充版本号,一般为00
    res = ver + pkhash

    # 计算两次sha256,所得结果的前8位作为校验值,填充到加密数据后
    res_dhash = double_sha256(res)
    res_dhash = res + res_dhash[:8]

    # base58编码
    res_b58 = single_base58(res_dhash)
    return res_b58

###########################################################################################################
# get_merkle_tree(merkle_leaves):
#     计算merkle tree，返回merkle tree全节点。最后一个节点为merkle root。
# params:
#     merkle_leaves:叶子节点。数据类型为:list
# return：
#     merkle tree全节点。数据类型为:list
###########################################################################################################
def get_merkle_tree(merkle_leaves):
    node_count = len(merkle_leaves)
    nodes = []
    for index in range(1, node_count + 1, 2):
        b1 = binascii.unhexlify(merkle_leaves[index - 1])[::-1]
        if index == node_count:
            b2 = binascii.unhexlify(merkle_leaves[index - 1])[::-1]
        else:
            b2 = binascii.unhexlify(merkle_leaves[index])[::-1]
        nodes.append(binascii.hexlify(sha256(sha256(b1 + b2).digest()).digest()[::-1]).decode())

    if len(nodes) != 1:
        new_nodes = get_merkle_tree(nodes)
        for n in new_nodes:
            merkle_leaves.append(n)
    else:
        merkle_leaves.append(nodes[0])
    return merkle_leaves

###########################################################################################################
# op_scriptsig_ecdsa_verify(sig,msg,pubkey,sigdecode = 'der'):
#     op_scriptsig验证，返回验证结果。
# params:
#     sig：签名数据。数据类型：str
#     msg：消息。数据类型：str
#     pubkey：公钥。数据类型：str
#     sigdecode：签名格式。默认为DER格式，数据类型：str
# return：
#     验证码结构。True or False
###########################################################################################################
def op_scriptsig_ecdsa_verify(sig,msg,pubkey,sigdecode = 'der'):
    try:
        if sigdecode == 'der':
            vk = VerifyingKey.from_string(bytes.fromhex(pubkey), curve=SECP256k1)
            res = vk.verify(binascii.unhexlify(sig.encode('ascii')), b(msg), hashfunc=hashlib.sha256,
                            sigdecode=util.sigdecode_der)
        else:
            vk = VerifyingKey.from_string(bytes.fromhex(pubkey), curve=SECP256k1)
            res = vk.verify(binascii.unhexlify(sig.encode('ascii')), b(msg), hashfunc=hashlib.sha256)
        return res
    except BadSignatureError:
        return False
    except Exception as ex:
        return False