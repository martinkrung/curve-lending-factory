#!/usr/bin/env python3

import os
import sys
import boa


RPC_ETHEREUM = os.getenv('RPC_ETHEREUM')
RPC_ARBITRUM = os.getenv('RPC_ARBITRUM')
ARBISCAN_API_KEY = os.getenv('ARBISCAN_API_KEY')
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')

boa.env.fork(RPC_ARBITRUM)


# from init tx of factory
stablecoin = "0x498Bf2B1e120FeD3ad3D42EA2165E9b73f99C1e5"
amm = "0xaA2377F39419F8f4CB98885076c41fE547C65a6A"
controller = "0xd5DCcBf65f0BC66934e1B2a7e515A35535f91B97"
vault = "0x104e15102E4Cf33e0e2cB7C304D406B523B04d7a"
pool_price_oracle = "0x57390a776A2312eF8BFc25e8624483303Dd8DfF8"
monetary_policy = "0x0b3536245faDABCF091778C4289caEbDc2c8f5C1"
gauge_factory = "0xabC000d88f23Bb45525E447528DBF656A9D55bf5"
admin = "0x452030a5D962d37D97A9D65487663cD5fd9C2B32"

local_factory = boa.load("contracts/lending/OneWayLendingFactoryL2.vy", stablecoin, amm, controller, vault, pool_price_oracle, monetary_policy, gauge_factory, admin)


amm_impl = local_factory.amm_impl()

# from init tx of tbtc market

print(f"amm_impl: {amm_impl}")
assert amm_impl == amm, "Test failed"

borrowed_token = "0x498Bf2B1e120FeD3ad3D42EA2165E9b73f99C1e5"
collateral_token = "0x6c84a8f1c29108F47a79964b5Fe888D4f4D0dE40"
A = 75
fee = 6000000000000000
loan_discount = 75000000000000000
liquidation_discount = 45000000000000000
price_oracle = "0x610D8284c0A8B5ecDe7Aaf36092B9Ac6c31477C9"
name = "tBTC-long2"
min_borrow_rate = 158548960
max_borrow_rate = 7927447995

new_market_vault = local_factory.create(
    borrowed_token,
    collateral_token,
    A,
    fee,
    loan_discount,
    liquidation_discount,
    price_oracle,
    name,
    min_borrow_rate,
    max_borrow_rate
)


print(f"new_market_vault: {new_market_vault}")
