# @version 0.4.0
"""
@title PlaceHolder
@author martinkrung for curve.fi
@license MIT
@notice placeholder contract
"""

arg1: public(address)


@deploy
def __init__( _arg1: address):
    """
    @notice Contract constructor
    @param _arg1 set _arg1 token address
    """
    self.arg1 = _arg1
