"""OpenGradient action provider."""

from typing import Any

from web3 import Web3

from ...network import Network
from ...wallet_providers import EvmWalletProvider
from ..action_decorator import create_action
from ..action_provider import ActionProvider
from coinbase_agentkit.action_providers.opengradient.schemas import (
    OpenGradientReadWorkflow,
)

import os
import opengradient as og

class OpenGradientActionProvider(ActionProvider):
    """Provides actions for interacting with OpenGradient."""

    def __init__(self, private_key: str | None = None, email: str | None = None, password: str | None = None):
        super().__init__("opengradient", [])

        private_key = private_key or os.getenv("OPENGRADIENT_PRIVATE_KEY")
        email = email or os.getenv("OPENGRADIENT_EMAIL")
        password = password or os.getenv("OPENGRADIENT_PASSWORD")

        if not private_key:
            raise ValueError("OPENGRADIENT_PRIVATE_KEY is not configured.")

        try:
            self.client = og.init(private_key=private_key, email=email, password=password)
        except Exception as e:
            raise ValueError(f"Failed to initialize OpenGradient client: {e}") from e

    @create_action(
        name="read_workflow",
        description="""
This tool allows users to read from a workflow smart contract on the OpenGradient network. 

TODO (KYLE)
The response from this tool should be a string representing...

Inputs:
- The smart contract address that is running the workflow
""",
        schema=OpenGradientReadWorkflow,
    )
    def read_workflow(self, args: dict[str, Any]) -> str:
        """Reads from a workflow on the OpenGradient network.

        Args:
            args (dict[str, Any]): Input arguments for the action.

        Returns:
            str: A message containing the action response or error details.

        """
        try:
            contract_address = args['contract_address']
            result = og.read_workflow_result(contract_address)

            number_tensors = {key: str(value) for key, value in result.numbers.items()}
            string_tensors = result.strings
            json_tensors = {key: str(value) for key, value in result.jsons.items()}

            # result = ""
            # if len(number_tensors) != 0:
            #     result += f"number tensors: {number_tensors}\n"
            # if len(string_tensors) != 0:
            #     result += f"string tensors: {string_tensors}\n"
            # if len(json_tensors) != 0:
            #     result += f"json tensors: {json_tensors}"

            return str(result)
        except Exception as e:
            return f"Error reading workflow: {e!s}"
        # try:
        #     superfluid_host_contract = Web3().eth.contract(
        #         address= , abi=CREATE_ABI
        #     )

        #     encoded_data = superfluid_host_contract.encode_abi(
        #         "createFlow",
        #         args=[
        #             args["token_address"],
        #             wallet_provider.get_address(),
        #             args["recipient"],
        #             int(args["flow_rate"]),
        #             "0x",
        #         ],
        #     )

        #     params = {"to": SUPERFLUID_HOST_ADDRESS, "data": encoded_data}

        #     tx_hash = wallet_provider.send_transaction(params)

        #     wallet_provider.wait_for_transaction_receipt(tx_hash)

        #     return f"Flow created successfully. Transaction hash: {tx_hash}"

        # except Exception as e:
        #     return f"Error creating flow: {e!s}"
        
    def supports_network(self, network: Network) -> bool:
        """Check if network is supported by OpenGradient actions.

        Args:
            network (Network): The network to check support for.

        Returns:
            bool: Whether the network is supported.

        """
        return network.protocol_family == "evm"


def opengradient_action_provider() -> OpenGradientActionProvider:
    """Create a new OpenGradient action provider.

    Returns:
        OpenGradientProvider: A new OpenGradient action provider instance.

    """
    return OpenGradientActionProvider()
