from brownie import Contract, chain, web3
import json
from pathlib import Path

abi = [{"name":"CommitOwnership","inputs":[{"type":"address","name":"admin","indexed":False}],"anonymous":False,"type":"event"},{"name":"ApplyOwnership","inputs":[{"type":"address","name":"admin","indexed":False}],"anonymous":False,"type":"event"},{"name":"Deposit","inputs":[{"type":"address","name":"provider","indexed":True},{"type":"uint256","name":"value","indexed":False},{"type":"uint256","name":"locktime","indexed":True},{"type":"int128","name":"type","indexed":False},{"type":"uint256","name":"ts","indexed":False}],"anonymous":False,"type":"event"},{"name":"Withdraw","inputs":[{"type":"address","name":"provider","indexed":True},{"type":"uint256","name":"value","indexed":False},{"type":"uint256","name":"ts","indexed":False}],"anonymous":False,"type":"event"},{"name":"Supply","inputs":[{"type":"uint256","name":"prevSupply","indexed":False},{"type":"uint256","name":"supply","indexed":False}],"anonymous":False,"type":"event"},{"outputs":[],"inputs":[{"type":"address","name":"token_addr"},{"type":"string","name":"_name"},{"type":"string","name":"_symbol"},{"type":"string","name":"_version"}],"stateMutability":"nonpayable","type":"constructor"},{"name":"commit_transfer_ownership","outputs":[],"inputs":[{"type":"address","name":"addr"}],"stateMutability":"nonpayable","type":"function","gas":37597},{"name":"apply_transfer_ownership","outputs":[],"inputs":[],"stateMutability":"nonpayable","type":"function","gas":38497},{"name":"commit_smart_wallet_checker","outputs":[],"inputs":[{"type":"address","name":"addr"}],"stateMutability":"nonpayable","type":"function","gas":36307},{"name":"apply_smart_wallet_checker","outputs":[],"inputs":[],"stateMutability":"nonpayable","type":"function","gas":37095},{"name":"get_last_user_slope","outputs":[{"type":"int128","name":""}],"inputs":[{"type":"address","name":"addr"}],"stateMutability":"view","type":"function","gas":2569},{"name":"user_point_history__ts","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"address","name":"_addr"},{"type":"uint256","name":"_idx"}],"stateMutability":"view","type":"function","gas":1672},{"name":"locked__end","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"address","name":"_addr"}],"stateMutability":"view","type":"function","gas":1593},{"name":"checkpoint","outputs":[],"inputs":[],"stateMutability":"nonpayable","type":"function","gas":37052342},{"name":"deposit_for","outputs":[],"inputs":[{"type":"address","name":"_addr"},{"type":"uint256","name":"_value"}],"stateMutability":"nonpayable","type":"function","gas":74279891},{"name":"create_lock","outputs":[],"inputs":[{"type":"uint256","name":"_value"},{"type":"uint256","name":"_unlock_time"}],"stateMutability":"nonpayable","type":"function","gas":74281465},{"name":"increase_amount","outputs":[],"inputs":[{"type":"uint256","name":"_value"}],"stateMutability":"nonpayable","type":"function","gas":74280830},{"name":"increase_unlock_time","outputs":[],"inputs":[{"type":"uint256","name":"_unlock_time"}],"stateMutability":"nonpayable","type":"function","gas":74281578},{"name":"withdraw","outputs":[],"inputs":[],"stateMutability":"nonpayable","type":"function","gas":37223566},{"name":"balanceOf","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"address","name":"addr"}],"stateMutability":"view","type":"function"},{"name":"balanceOf","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"address","name":"addr"},{"type":"uint256","name":"_t"}],"stateMutability":"view","type":"function"},{"name":"balanceOfAt","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"address","name":"addr"},{"type":"uint256","name":"_block"}],"stateMutability":"view","type":"function","gas":514333},{"name":"totalSupply","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function"},{"name":"totalSupply","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"uint256","name":"t"}],"stateMutability":"view","type":"function"},{"name":"totalSupplyAt","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"uint256","name":"_block"}],"stateMutability":"view","type":"function","gas":812560},{"name":"changeController","outputs":[],"inputs":[{"type":"address","name":"_newController"}],"stateMutability":"nonpayable","type":"function","gas":36907},{"name":"token","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":1841},{"name":"supply","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":1871},{"name":"locked","outputs":[{"type":"int128","name":"amount"},{"type":"uint256","name":"end"}],"inputs":[{"type":"address","name":"arg0"}],"stateMutability":"view","type":"function","gas":3359},{"name":"epoch","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":1931},{"name":"point_history","outputs":[{"type":"int128","name":"bias"},{"type":"int128","name":"slope"},{"type":"uint256","name":"ts"},{"type":"uint256","name":"blk"}],"inputs":[{"type":"uint256","name":"arg0"}],"stateMutability":"view","type":"function","gas":5550},{"name":"user_point_history","outputs":[{"type":"int128","name":"bias"},{"type":"int128","name":"slope"},{"type":"uint256","name":"ts"},{"type":"uint256","name":"blk"}],"inputs":[{"type":"address","name":"arg0"},{"type":"uint256","name":"arg1"}],"stateMutability":"view","type":"function","gas":6079},{"name":"user_point_epoch","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"address","name":"arg0"}],"stateMutability":"view","type":"function","gas":2175},{"name":"slope_changes","outputs":[{"type":"int128","name":""}],"inputs":[{"type":"uint256","name":"arg0"}],"stateMutability":"view","type":"function","gas":2166},{"name":"controller","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2081},{"name":"transfersEnabled","outputs":[{"type":"bool","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2111},{"name":"name","outputs":[{"type":"string","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":8543},{"name":"symbol","outputs":[{"type":"string","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":7596},{"name":"version","outputs":[{"type":"string","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":7626},{"name":"decimals","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2231},{"name":"future_smart_wallet_checker","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2261},{"name":"smart_wallet_checker","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2291},{"name":"admin","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2321},{"name":"future_admin","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2351}]

snapshot_block = 12059299
# some vecrv holders use bespoke setups which cannot be easily replicated on another chain, replace them with an eoa
# make sure all addresses are lower case, not checksummed
replacements = {
    "0xf147b8125d2ef93fb6965db97d6746952a133934": "0x2d407ddb06311396fe14d4b49da5f0471447d45c",  # yearn.finance
}


def main():
    ve = web3.eth.contract('0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2', abi=abi)
    vecrv = Contract.from_abi('veCRV', ve.address, ve.abi)

    datafile = Path('data.json')
    if datafile.exists():
        with datafile.open() as fp:
            data = json.load(fp)
            start_block = data['latest']
    else:
        start_block = 10647812
        data = {'addresses': {}}

    lockers = set(data['addresses'])
    for height in range(start_block, snapshot_block+1, 10000):
        print(f"{height}/{snapshot_block}")
        lockers.update(i.args.provider for i in ve.events.Deposit().getLogs(fromBlock=height, toBlock=height+10000))
    lockers = sorted(lockers)
    print(f"\nFound {len(lockers)} addresses!")

    mc_data = [[str(vecrv), vecrv.balanceOf.encode_input(addr)] for addr in lockers]
    multicall = Contract('0x5e227AD1969Ea493B43F840cfF78d08a6fc17796')

    data = {'latest': snapshot_block, 'addresses': {}}
    step = 1000
    for i in range(0, len(mc_data), step):
        print(f"{i}/{len(mc_data)}")
        response = multicall.aggregate.call(mc_data[i:i+step], block_identifier=snapshot_block)[1]
        decoded = [vecrv.balanceOf.decode_output(data) for data in response]
        data['addresses'].update({addr.lower(): balance for addr, balance in zip(lockers[i:i+step], decoded)})
    for original, new in replacements.items():
       data['addresses'].setdefault(new, 0)
       data['addresses'][new] += data['addresses'].pop(original)

    json.dump(data, datafile.open('w'))
    print(sum(data['addresses'].values())-vecrv.totalSupply[()](block_identifier=snapshot_block))
