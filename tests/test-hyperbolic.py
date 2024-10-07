#!/usr/bin/env python3

import os
import sys
import boa


RPC_ETHEREUM = os.getenv('RPC_ETHEREUM')
RPC_ARBITRUM = os.getenv('RPC_ARBITRUM')
ARBISCAN_API_KEY = os.getenv('ARBISCAN_API_KEY')
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')

'''
    alpha = 0.01 # < 1, if 0.1, than rate is 0.5%/0.05 at 0% utilization  (0.1 * 0.1 = 0.01) and r0 = 0.1
    beta = 2.5 # > 1, if 2.5, than rate is 25%/0.25 at 100% utilization and r0 = 0.1
    u0 = 0.9 # target utilization, at this point rate is 0.10%, as r0 = 0.1
    r0 = 0.1 # target rate of pool, set fixed at 0.1

    'u_inf' : 1.079136690647482,
    'r_minf' : -0.18705035971223008,
    'A' : 0.2126442730707519,
'''

boa.env.fork(RPC_ETHEREUM) 

# https://etherscan.io/address/0x188041ad83145351ef45f4bb91d08886648aeaf8#code


target_utilization = 900000000000000000 # 90% / 10**18
target_rate = int(0.1 * 10 ** 10) # 10% / 10**10
low_ratio = 150000000000000000  # 15% / 10**18 : 0.15 * 0.1 = 0.015 at u = 0
high_ratio = 3000000000000000000 # 300% / 10**18 : 300 * 0.1 = 0.30 at u = 100%
rate_shift = 0

WBTC = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"

hyperbolic = boa.load('contracts/mpolicies/HyperbolicMonetaryPolicy.vy', WBTC, target_utilization, target_rate, low_ratio, high_ratio, rate_shift)

print(f"hyperbolic.parameters(): {hyperbolic.parameters()}")
print(f"hyperbolic.parameters(): [r_0, u_inf, A, r_minf, shift]")


for u in range(0, 1000000000000000001, 10000000000000000):
    # print(f"U hyperbolic.calculate_rate_test({u}): {hyperbolic.calculate_rate_test(u)}")
    print(f"utilization: ({u/10**18}): rate {hyperbolic.calculate_rate_test(u)/10**10}")

'''
from https://lend.curve.fi/#/ethereum/markets/one-way-market-9/ 
WBTC-crvUSD
Arg [3] : target_utilization (uint256): 850000000000000000 # 85% / 10**18
Arg [4] : low_ratio (uint256): 500000000000000000 # 5% / 10**19
Arg [5] : high_ratio (uint256): 3000000000000000000 # 30% / 10**19
Arg [6] : rate_shift (uint256): 0
'''
# from on-chain
# https://etherscan.io/address/0xE0438Eb3703bF871E31Ce639bd351109c88666ea#readContract#F28




amm = boa.from_etherscan(
    0xE0438Eb3703bF871E31Ce639bd351109c88666ea,
    name="AMM",
    uri="https://api.etherscan.io/api",
    api_key=ETHERSCAN_API_KEY
)

target_rate = amm.rate()
print(f"target_rate: {target_rate}")
print(f"target_rate: {target_rate/10**10}")


target_utilization = 850000000000000000 # 90% / 10**18
#target_rate = int(0.1 * 10 ** 10) # 10% / 10**10
low_ratio = 500000000000000000  # 15% / 10**18 : 0.15 * 0.1 = 0.015 at u = 0
high_ratio = 3000000000000000000 # 300% / 10**18 : 300 * 0.1 = 0.30 at u = 100%
rate_shift = 0

hyperbolic = boa.load('contracts/mpolicies/HyperbolicMonetaryPolicy.vy', WBTC, target_utilization, target_rate, low_ratio, high_ratio, rate_shift)

print(f"hyperbolic.parameters(): {hyperbolic.parameters()}")
print(f"hyperbolic.parameters(): [r_0, u_inf, A, r_minf, shift]")


for u in range(0, 1000000000000000001, 10000000000000000):
    # print(f"hyperbolic.calculate_rate_test({u}): {hyperbolic.calculate_rate_test(u)}")
    print(f"utilization: ({u/10**18}): rate {hyperbolic.calculate_rate_test(u)/10**10}")


# at 85% utilization, rate should be 39%
u0 = target_utilization
r0 = target_rate
print(f"hyperbolic.calculate_rate_test(85%): {hyperbolic.calculate_rate_test(u0)}")
print(f"hyperbolic.calculate_rate_test(85%): {hyperbolic.calculate_rate_test(u0)/10**10}")

# Updated assertion to include variance of +5/-5
expected_rate = hyperbolic.calculate_rate_test(u0)
assert expected_rate >= r0 - 5 and expected_rate <= r0 + 5, f"Test failed: expected rate within {r0 - 5} and {r0 + 5}, got {expected_rate}"

# from existing WBTC-crvUSD market, with SecondaryMonetaryPolicy
monetary_policy = boa.from_etherscan(
    0x188041ad83145351ef45f4bb91d08886648aeaf8,
    name="MonetaryPolicy",
    uri="https://api.etherscan.io/api",
    api_key=ETHERSCAN_API_KEY
)

print(f"monetary_policy.parameters(): {monetary_policy.parameters()}")
print(f"monetary_policy.parameters(): [u_inf,A,r_minf,shift]")

# https://etherscan.io/address/0xcad85b7fe52b1939dceebee9bcf0b2a5aa0ce617

CONTROLLER_ADDRESS = "0xcad85b7fe52b1939dceebee9bcf0b2a5aa0ce617"

print(f"monetary_policy.rate(CONTROLLER_ADDRESS): {monetary_policy.rate(CONTROLLER_ADDRESS)}")
print(f"monetary_policy.rate(CONTROLLER_ADDRESS): {monetary_policy.rate(CONTROLLER_ADDRESS)/10**10}")
