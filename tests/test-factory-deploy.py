#!/usr/bin/env python3

import os
import sys
import boa


RPC_ETHEREUM = os.getenv('RPC_ETHEREUM')
RPC_ARBITRUM = os.getenv('RPC_ARBITRUM')
RPC_OPTIMISM = os.getenv('RPC_OPTIMISM')
ARBISCAN_API_KEY = os.getenv('ARBISCAN_API_KEY')
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')

boa.env.fork(RPC_OPTIMISM)

blueprint = boa.load_partial("contracts/mpolicies/SemilogMonetaryPolicy.vy")
monetary_policy_semilog_impl = blueprint.deploy_as_blueprint()

print(f"monetary_policy_semilog_impl: {monetary_policy_semilog_impl}")

blueprint = boa.load_partial("contracts/mpolicies/HyperbolicMonetaryPolicy.vy")
monetary_policy_hyperbolic_impl = blueprint.deploy_as_blueprint() 

print(f"monetary_policy_hyperbolic_impl: {monetary_policy_hyperbolic_impl}")


# from init tx of factory
# https://optimistic.etherscan.io/address/0x5ea8f3d674c70b020586933a0a5b250734798bef#code
stablecoin = "0xC52D7F23a2e460248Db6eE192Cb23dD12bDDCbf6"
amm = "0x40b8c0c9186eAEaf84023d81CD2a709e81fCFbC1"
controller = "0xCc65F473815c97bDe543Db458358F09852eDb5B4"
vault = "0x3B1DF11b96b2F5525aBe75eebeFb1ce0928d2411"
pool_price_oracle = "0x227c9AD884e0E32a698FB38ba0511eE36fA92b7d"
# monetary_policy = "0xa2294769e9CFA9Fd029030F7be94E2602821677B"
gauge_factory = "0xabC000d88f23Bb45525E447528DBF656A9D55bf5"
admin = "0x28c4A1Fa47EEE9226F8dE7D6AF0a41C62Ca98267"


local_factory_dynamic = boa.load("contracts/lending/OneWayLendingFactoryL2TwoMp.vy", stablecoin, amm, controller, vault, pool_price_oracle,
                                 monetary_policy_semilog_impl, monetary_policy_hyperbolic_impl, gauge_factory, admin)

# value from this tx
# https://optimistic.etherscan.io/tx/0x712644bbf1970648f49a1991530b3dbe5179d190ceaf96ae7100c0de04c80920
borrowed_token = "0xC52D7F23a2e460248Db6eE192Cb23dD12bDDCbf6"
collateral_token = "0x4200000000000000000000000000000000000006"
A = 70
fee = 6000000000000000
loan_discount = 70000000000000000
liquidation_discount = 40000000000000000
price_oracle = "0x92577943c7aC4accb35288aB2CC84D75feC330aF"
name = "ETH-long"
min_borrow_rate = 634195839
max_borrow_rate = 9512937595
supply_limit = 115792089237316195423570985008687907853269984665640564039457584007913129639935

new_market_vault = local_factory_dynamic.create(
    borrowed_token,
    collateral_token,
    A,
    fee,
    loan_discount,
    liquidation_discount,
    price_oracle,
    name,
    [min_borrow_rate, max_borrow_rate],
    supply_limit
)

print(f"new_market_vault: {new_market_vault}")

monetary_policy_address = local_factory_dynamic.monetary_policies(0)

monetary_policy = boa.load_partial("contracts/mpolicies/SemilogMonetaryPolicy.vy").at(monetary_policy_address)

assert monetary_policy.min_rate() == min_borrow_rate
assert monetary_policy.max_rate() == max_borrow_rate

print(f"monetary_policy.min_rate(): {monetary_policy.min_rate()}")
print(f"monetary_policy.max_rate(): {monetary_policy.max_rate()}")


## deploy with hyperbolic monetary policy


print(f"local_factory_dynamic.monetary_policy_hyperbolic_impl: {local_factory_dynamic.monetary_policy_hyperbolic_impl()}")

target_utilization = 900000000000000000 # 90% / 10**18
target_rate = int(0.1 * 10 ** 10) # 10% / 10**10
low_ratio = 150000000000000000  # 15% / 10**18 : 0.15 * 0.1 = 0.015 at u = 0
high_ratio = 3000000000000000000 # 300% / 10**18 : 300 * 0.1 = 0.30 at u = 100%
rate_shift = 0

u0 = target_utilization
r0 = target_rate
alpha = low_ratio
beta = high_ratio

borrowed_token = "0xC52D7F23a2e460248Db6eE192Cb23dD12bDDCbf6"
collateral_token = "0x4200000000000000000000000000000000000006"
A = 70
fee = 6000000000000000
loan_discount = 70000000000000000
liquidation_discount = 40000000000000000
price_oracle = "0x92577943c7aC4accb35288aB2CC84D75feC330aF"
name = "ETH-long2"
supply_limit = 115792089237316195423570985008687907853269984665640564039457584007913129639935

new_market_vault = local_factory_dynamic.create(
    borrowed_token,
    collateral_token,
    A,
    fee,
    loan_discount,
    liquidation_discount,
    price_oracle,
    name,
    [target_utilization, target_rate, low_ratio, high_ratio, rate_shift],
    supply_limit
)

print(f"new_market_vault: {new_market_vault}")

monetary_policy_address = local_factory_dynamic.monetary_policies(1)

monetary_policy = boa.load_partial("contracts/mpolicies/HyperbolicMonetaryPolicy.vy").at(monetary_policy_address)

parameters = monetary_policy.parameters()

print(f"parameters: {parameters}")
print(f"parameters: [r_0, u_inf, A, r_minf, shift]")

assert monetary_policy.parameters()[0] == target_rate
assert monetary_policy.parameters()[4] == rate_shift
