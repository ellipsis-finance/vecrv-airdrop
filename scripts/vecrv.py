from brownie import Contract, chain, web3
import json
from pathlib import Path
import time
from itertools import zip_longest
from collections import deque
from fractions import Fraction
from eth_abi.packed import encode_abi_packed
from eth_utils import encode_hex

abi = [{"name":"CommitOwnership","inputs":[{"type":"address","name":"admin","indexed":False}],"anonymous":False,"type":"event"},{"name":"ApplyOwnership","inputs":[{"type":"address","name":"admin","indexed":False}],"anonymous":False,"type":"event"},{"name":"Deposit","inputs":[{"type":"address","name":"provider","indexed":True},{"type":"uint256","name":"value","indexed":False},{"type":"uint256","name":"locktime","indexed":True},{"type":"int128","name":"type","indexed":False},{"type":"uint256","name":"ts","indexed":False}],"anonymous":False,"type":"event"},{"name":"Withdraw","inputs":[{"type":"address","name":"provider","indexed":True},{"type":"uint256","name":"value","indexed":False},{"type":"uint256","name":"ts","indexed":False}],"anonymous":False,"type":"event"},{"name":"Supply","inputs":[{"type":"uint256","name":"prevSupply","indexed":False},{"type":"uint256","name":"supply","indexed":False}],"anonymous":False,"type":"event"},{"outputs":[],"inputs":[{"type":"address","name":"token_addr"},{"type":"string","name":"_name"},{"type":"string","name":"_symbol"},{"type":"string","name":"_version"}],"stateMutability":"nonpayable","type":"constructor"},{"name":"commit_transfer_ownership","outputs":[],"inputs":[{"type":"address","name":"addr"}],"stateMutability":"nonpayable","type":"function","gas":37597},{"name":"apply_transfer_ownership","outputs":[],"inputs":[],"stateMutability":"nonpayable","type":"function","gas":38497},{"name":"commit_smart_wallet_checker","outputs":[],"inputs":[{"type":"address","name":"addr"}],"stateMutability":"nonpayable","type":"function","gas":36307},{"name":"apply_smart_wallet_checker","outputs":[],"inputs":[],"stateMutability":"nonpayable","type":"function","gas":37095},{"name":"get_last_user_slope","outputs":[{"type":"int128","name":""}],"inputs":[{"type":"address","name":"addr"}],"stateMutability":"view","type":"function","gas":2569},{"name":"user_point_history__ts","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"address","name":"_addr"},{"type":"uint256","name":"_idx"}],"stateMutability":"view","type":"function","gas":1672},{"name":"locked__end","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"address","name":"_addr"}],"stateMutability":"view","type":"function","gas":1593},{"name":"checkpoint","outputs":[],"inputs":[],"stateMutability":"nonpayable","type":"function","gas":37052342},{"name":"deposit_for","outputs":[],"inputs":[{"type":"address","name":"_addr"},{"type":"uint256","name":"_value"}],"stateMutability":"nonpayable","type":"function","gas":74279891},{"name":"create_lock","outputs":[],"inputs":[{"type":"uint256","name":"_value"},{"type":"uint256","name":"_unlock_time"}],"stateMutability":"nonpayable","type":"function","gas":74281465},{"name":"increase_amount","outputs":[],"inputs":[{"type":"uint256","name":"_value"}],"stateMutability":"nonpayable","type":"function","gas":74280830},{"name":"increase_unlock_time","outputs":[],"inputs":[{"type":"uint256","name":"_unlock_time"}],"stateMutability":"nonpayable","type":"function","gas":74281578},{"name":"withdraw","outputs":[],"inputs":[],"stateMutability":"nonpayable","type":"function","gas":37223566},{"name":"balanceOf","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"address","name":"addr"}],"stateMutability":"view","type":"function"},{"name":"balanceOf","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"address","name":"addr"},{"type":"uint256","name":"_t"}],"stateMutability":"view","type":"function"},{"name":"balanceOfAt","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"address","name":"addr"},{"type":"uint256","name":"_block"}],"stateMutability":"view","type":"function","gas":514333},{"name":"totalSupply","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function"},{"name":"totalSupply","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"uint256","name":"t"}],"stateMutability":"view","type":"function"},{"name":"totalSupplyAt","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"uint256","name":"_block"}],"stateMutability":"view","type":"function","gas":812560},{"name":"changeController","outputs":[],"inputs":[{"type":"address","name":"_newController"}],"stateMutability":"nonpayable","type":"function","gas":36907},{"name":"token","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":1841},{"name":"supply","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":1871},{"name":"locked","outputs":[{"type":"int128","name":"amount"},{"type":"uint256","name":"end"}],"inputs":[{"type":"address","name":"arg0"}],"stateMutability":"view","type":"function","gas":3359},{"name":"epoch","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":1931},{"name":"point_history","outputs":[{"type":"int128","name":"bias"},{"type":"int128","name":"slope"},{"type":"uint256","name":"ts"},{"type":"uint256","name":"blk"}],"inputs":[{"type":"uint256","name":"arg0"}],"stateMutability":"view","type":"function","gas":5550},{"name":"user_point_history","outputs":[{"type":"int128","name":"bias"},{"type":"int128","name":"slope"},{"type":"uint256","name":"ts"},{"type":"uint256","name":"blk"}],"inputs":[{"type":"address","name":"arg0"},{"type":"uint256","name":"arg1"}],"stateMutability":"view","type":"function","gas":6079},{"name":"user_point_epoch","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"address","name":"arg0"}],"stateMutability":"view","type":"function","gas":2175},{"name":"slope_changes","outputs":[{"type":"int128","name":""}],"inputs":[{"type":"uint256","name":"arg0"}],"stateMutability":"view","type":"function","gas":2166},{"name":"controller","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2081},{"name":"transfersEnabled","outputs":[{"type":"bool","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2111},{"name":"name","outputs":[{"type":"string","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":8543},{"name":"symbol","outputs":[{"type":"string","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":7596},{"name":"version","outputs":[{"type":"string","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":7626},{"name":"decimals","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2231},{"name":"future_smart_wallet_checker","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2261},{"name":"smart_wallet_checker","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2291},{"name":"admin","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2321},{"name":"future_admin","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2351}]

# some vecrv holders use bespoke setups which cannot be easily replicated on another chain, replace them with an eoa
# make sure all addresses are lower case, not checksummed
replacements = {
    "0xf147b8125d2ef93fb6965db97d6746952a133934": "0x2d407ddb06311396fe14d4b49da5f0471447d45c",  # yearn.finance
    "0x52f541764e6e90eebc5c21ff570de0e2d63766b6": "0xb36a0671b3d49587236d7833b01e79798175875f", # stakedao
    "0x989aeb4d175e16225e39e87d0d97a3360524ad80": "0x947b7742c403f20e5faccdac5e092c943e7d0277" # convex finance
}



class MerkleTree:
    def __init__(self, elements):
        self.elements = sorted(set(web3.keccak(hexstr=el) for el in elements))
        self.layers = MerkleTree.get_layers(self.elements)

    @property
    def root(self):
        return self.layers[-1][0]

    def get_proof(self, el):
        el = web3.keccak(hexstr=el)
        idx = self.elements.index(el)
        proof = []
        for layer in self.layers:
            pair_idx = idx + 1 if idx % 2 == 0 else idx - 1
            if pair_idx < len(layer):
                proof.append(encode_hex(layer[pair_idx]))
            idx //= 2
        return proof

    @staticmethod
    def get_layers(elements):
        layers = [elements]
        while len(layers[-1]) > 1:
            layers.append(MerkleTree.get_next_layer(layers[-1]))
        return layers

    @staticmethod
    def get_next_layer(elements):
        return [MerkleTree.combined_hash(a, b) for a, b in zip_longest(elements[::2], elements[1::2])]

    @staticmethod
    def combined_hash(a, b):
        if a is None:
            return b
        if b is None:
            return a
        return web3.keccak(b''.join(sorted([a, b])))


def get_vecrv_addresses(addresses, start_block):
    vecrv = Contract('0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2')
    ve = web3.eth.contract(vecrv.address, abi=vecrv.abi)

    addresses = set(addresses)
    latest = chain[-1].number
    for height in range(start_block, latest+1, 10000):
        print(f"{height}/{latest}")
        addresses.update(i.args.provider for i in ve.events.Deposit().getLogs(fromBlock=height, toBlock=height+10000))

    print(f"\nFound {len(addresses)} addresses!")
    return sorted(addresses), latest


def get_block_at_timestamp(timestamp):
    current = chain[-1]

    high = current.number - (current.timestamp - timestamp) // 15
    low = current.number - (current.timestamp - timestamp) // 11

    while low <= high:
        middle = low + (high - low) // 2
        block = chain[middle]
        if block.timestamp >= timestamp and chain[middle-1].timestamp < timestamp:
            return middle
        elif block.timestamp < timestamp:
            low = middle + 1
        else:
            high = middle - 1
    raise ValueError


def get_vecrv_balances(addresses, snapshot_block):
    vecrv = Contract('0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2')
    mc_data = [[str(vecrv), vecrv.balanceOf.encode_input(addr)] for addr in addresses]
    multicall = Contract('0x5e227AD1969Ea493B43F840cfF78d08a6fc17796')

    balances = {}
    step = 1000
    for i in range(0, len(mc_data), step):
        print(f"{i}/{len(mc_data)}")
        response = multicall.aggregate.call(mc_data[i:i+step], block_identifier=snapshot_block)[1]
        decoded = [vecrv.balanceOf.decode_output(data) for data in response]
        balances.update({addr.lower(): balance for addr, balance in zip(addresses[i:i+step], decoded)})
    for original, new in replacements.items():
       balances.setdefault(new, 0)
       balances[new] += balances.pop(original)
    print(sum(balances.values())-vecrv.totalSupply[()](block_identifier=snapshot_block))
    return balances


def get_proof(balances, snapshot_block):
    total_distribution = (250000000*10**18)//52
    total_vecrv = sum(balances.values())
    balances = {k: int(Fraction(v*total_distribution, total_vecrv)) for k, v in balances.items()}
    balances = {k: v for k, v in balances.items() if v}

    # handle any rounding errors
    addresses = deque(balances)
    while sum(balances.values()) < total_distribution:
        balances[addresses[0]] += 1
        addresses.rotate()

    assert sum(balances.values()) == total_distribution

    elements = [(index, account, balances[account]) for index, account in enumerate(sorted(balances))]
    nodes = [encode_hex(encode_abi_packed(['uint', 'address', 'uint'], el)) for el in elements]
    tree = MerkleTree(nodes)
    distribution = {
        'merkleRoot': encode_hex(tree.root),
        'tokenTotal': hex(sum(balances.values())),
        'blockHeight': snapshot_block,
        'claims': {
            user: {'index': index, 'amount': hex(amount), 'proof': tree.get_proof(nodes[index])}
            for index, user, amount in elements
        },
    }
    print(f'merkle root: {encode_hex(tree.root)}')
    return distribution


def main():
    address_json = Path('addresses.json')
    if address_json.exists():
        with address_json.open() as fp:
            data = json.load(fp)
            start_block = data['latest']
            addresses = data['addresses']
    else:
        start_block = 10647812
        addresses = []
    addresses, height = get_vecrv_addresses(addresses, start_block)
    with address_json.open('w') as fp:
        json.dump({'addresses': addresses, 'latest': height}, fp)

    snapshot_time = int((time.time() // 604800) * 604800)
    snapshot_block = get_block_at_timestamp(snapshot_time)
    balances = get_vecrv_balances(addresses, snapshot_block)
    distribution = get_proof(balances, snapshot_block)

    date = time.strftime("%Y-%m-%d", time.gmtime(snapshot_time))
    distro_json = Path(f'distributions/distribution-{date}.json')

    with distro_json.open('w') as fp:
        json.dump(distribution, fp)
    print(f"Distribution saved to {distro_json}")
