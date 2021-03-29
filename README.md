# vecrv-airdrop

Snapshots are taken on the first block mined at the start of the new epoch week (midnight Thursday, GMT). The snapshot is generated independently by the Ellipsis and Curve teams. The proof is submitted on-chain by Ellipsis, verified and approved by Curve. New snapshots should be available for claim within 24 hours after they are taken.

To generate the proof for the current week's snapshot:

```bash
brownie run vecrv
```

The distributor contract is deployed on BSC at [`0x60a8AD8470189033789c1053B0c6F89eB27Bca18`](https://bscscan.com/address/0x60a8AD8470189033789c1053B0c6F89eB27Bca18#code)

Snapshots will be added to [`distributions`](distributions) within this repo as they are are completed.
