from collections.abc import Callable
from decimal import Decimal

from pydantic import BaseModel, Field

from cdp_agentkit_core.actions import CdpAction
from cdp_agentkit_core.actions.morpho.constants import METAMORPHO_ABI
from cdp_agentkit_core.actions.utils import approve

import opengradient as og

RUN_MODEL_PROMPT = """
This tool allows depositing assets into a Morpho Vault.
It takes:

- vault_address: The address of the Morpho Vault to deposit to
- assets: The amount of assets to deposit in whole units
    Examples for WETH:
    - 1 WETH
    - 0.1 WETH
    - 0.01 WETH
- receiver: The address to receive the shares
- token_address: The address of the token to approve

Important notes:
- Make sure to use the exact amount provided. Do not convert units for assets for this action.
- Please use a token address (example 0x4200000000000000000000000000000000000006) for the token_address field. If you are unsure of the token address, please clarify what the requested token address is before continuing.
"""

class OpenGradientRunModelInput(BaseModel):
    """Input schema for Morpho Vault deposit action."""

    assets: str = Field(..., description="The quantity of assets to deposit, in whole units")
    receiver: str = Field(
        ...,
        description="The address that will own the position on the vault which will receive the shares",
    )
    token_address: str = Field(
        ..., description="The address of the assets token to approve for deposit"
    )
    vault_address: str = Field(..., description="The address of the Morpho Vault to deposit to")


def run_model(
    vault_address: str,
    assets: str,
    receiver: str,
    token_address: str,
) -> str:
    """Deposit assets into a Morpho Vault.

    Args:
        wallet (Wallet): The wallet to execute the deposit from
        vault_address (str): The address of the Morpho Vault
        assets (str): The amount of assets to deposit in whole units (e.g., 0.01 WETH)
        receiver (str): The address to receive the shares
        token_address (str): The address of the token to approve

    Returns:
        str: A success message with transaction hash or error message

    """
    return "Done"


class OpenGradientRunModelAction(CdpAction):
    """OpenGradient run model action."""

    name: str = "og_run_model"
    description: str = RUN_MODEL_PROMPT
    args_schema: type[BaseModel] = OpenGradientRunModelInput
    func: Callable[..., str] = run_model
