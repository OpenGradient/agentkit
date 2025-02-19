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
import coinbase_agentkit.action_providers.opengradient.constants

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
This tool reads workflow execution results from smart contracts deployed on the OpenGradient network.
Use this tool specifically for retrieving workflow data and results - do not use it for writing or modifying workflow states.

Inputs:
- contract_address: A string containing the OpenGradient smart contract address where the workflow results are stored (e.g. "0x1234...")

Outputs:
- A "ModelOuptut" string with three relevant tensors (arrays of values):
    1. numbers -- This is a dictionary of number tensors
    2. strings -- This is a dictionary of string tensors
    3. jsons -- This is a dictionary of JSON tensors

Example output:
ModelOutput(numbers={'Y': array([0.02208495], dtype=float32)}, strings={}, jsons={}, is_simulation_result=False)

Important notes:
- The contract address must be a valid Ethereum address format (0x followed by 40 hexadecimal characters)
- This is a read-only operation and will not modify any blockchain state
- Returns workflow results in their native format as stored on the blockchain
- Will return an error if:
  - The contract address is invalid
  - The contract does not exist on the OpenGradient network
  - The contract is not a valid workflow contract
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

            return str(result)
        except Exception as e:
            return f"Error reading workflow: {e!s}"
        
    @create_action(
        name="read_workflow_eth_usdt_one_hour_volatility_forecast",
        description="""
This tool reads the latest ETH/USDT 1-hour volatility prediction from a model deployment on the OpenGradient network. 
The model forecasts the standard deviation of 1-minute returns for ETH/USDT over the next hour.

Inputs:
- The model's inputs are handled automatically by oracles - no user input is required.

Outputs:
- This model outputs a single float value representing the predicted standard deviation
Example output format: 0.00037741573760285974

Important notes:
- This is a read-only operation and will not modify any blockchain state
- The prediction is automatically updated hourly with the 10 most recent 3-minute OHLC candles from oracle-fed data
""",
        schema=OpenGradientReadWorkflow,
    )
    def read_workflow_eth_usdt_one_hour_volatility_forecast(self, args: dict[str, Any]) -> str:
        """Reads from the ETH/USDT one hour volatility forecast model workflow on the OpenGradient network.

        Args:
            args (dict[str, Any]): Input arguments for the action.

        Returns:
            str: A message containing the action response or error details.

        """
        try:
            contract_address = constants.ETH_USDT_ONE_HOUR_VOLATILITY_ADDRESS
            result = og.read_workflow_result(contract_address)

            return str(result.numbers["Y"])
        except Exception as e:
            return f"Error reading one_hour_eth_usdt_volatility workflow: {e!s}"
        
    @create_action(
        name="read_workflow_sui_usdt_six_hour_return_forecast",
        description="""
This tool reads the latest SUI/USDT 6-hour return forecast from a model deployment on the OpenGradient network. 
The model predicts the expected price return over the next 6 hours for the SUI/USDT trading pair.

Inputs:
- The model's inputs are handled automatically by oracles - no user input is required.

Outputs:
- This model outputs a single float value representing the predicted 6-hour return
Example output format: -0.10838824510574341 (represents approximately -10.84% predicted return)

Important notes:
- This is a read-only operation and will not modify any blockchain state
- The prediction is automatically updated with the 6 most recent 3-hour OHLC candles using oracle-fed data
""",
        schema=OpenGradientReadWorkflow,
    )
    def read_workflow_sui_usdt_six_hour_return_forecast(self, args: dict[str, Any]) -> str:
        """Reads from the SUI/USDT six hour return forecast workflow on the OpenGradient network.

        Args:
            args (dict[str, Any]): Input arguments for the action.

        Returns:
            str: A message containing the action response or error details.

        """
        try:
            contract_address = constants.SUI_USDT_SIX_HOUR_FORECAST_ADDRESS
            result = og.read_workflow_result(contract_address)

            return str(result.numbers["destandardized_prediction"])
        except Exception as e:
            return f"Error reading one_hour_eth_usdt_volatility workflow: {e!s}"
        
    @create_action(
        name="read_workflow_sui_usdt_30_minute_return_forecast",
        description="""
This tool reads the latest SUI/USDT 30-minute return forecast from a model deployment on the OpenGradient network.
The model predicts the expected price return over the next 30 minutes for the SUI/USDT trading pair.

Inputs:
- The model's inputs are handled automatically by oracles - no user input is required.

Outputs:
- This model outputs a single float value representing the predicted 30-minute return
Example output format: -0.03255799412727356 (represents approximately -3.26% predicted return)

Important notes:
- This is a read-only operation and will not modify any blockchain state
- The prediction is automatically updated with a rolling window of recent OHLC price data from the last 10 minutes using oracle-fed data
""",
        schema=OpenGradientReadWorkflow,
    )
    def read_workflow_sui_usdt_30_minute_return_forecast(self, args: dict[str, Any]) -> str:
        """Reads from the SUI/USDT 30 minute return forecast workflow on the OpenGradient network.

        Args:
            args (dict[str, Any]): Input arguments for the action.

        Returns:
            str: A message containing the action response or error details.

        """
        try:
            contract_address = constants.SUI_USDT_THIRTY_MIN_FORECAST_ADDRES
            result = og.read_workflow_result(contract_address)

            return str(result.numbers["destandardized_prediction"])
        except Exception as e:
            return f"Error reading one_hour_eth_usdt_volatility workflow: {e!s}"
        
    @create_action(
        name="prompt_dobby",
        description="""
This tool generates responses using the Dobby-Mini-Unhinged-Llama-3.1-8B model, a language model with a focus on crypto-positive and pro-freedom responses. 
Do not use this tool for other LLM models or prompt formats.

Inputs:
- prompt: String containing the input prompt for the model
- temperature: (Optional, default=0.95) Float between 0.0 and 2.0 controlling randomness (higher = more random)
- max_tokens: (Optional, default=2048) Integer specifying maximum length of generated response

Output:
- Returns a string containing just the model's response text
Example output: "Listen up, Bitcoin isn't just some random internet money - it's a middle finger to centralized banking. Sure, the price swings like crazy, but that's the cost of true financial freedom. Do your own research, but don't sleep on crypto's potential to change everything."

Important notes:
- The model has strong inherent biases towards:
  - Pro-cryptocurrency narratives
  - Personal freedom and decentralization
  - Direct, unfiltered communication style
- Responses will maintain these stances even when prompted otherwise
- Model uses a more casual, blunt tone compared to typical AI assistants
- Temperature controls response variability:
  - 0.0: Most deterministic
  - 0.7: Balanced creativity (recommended)
  - 2.0: Maximum randomness
- Response content may include strong opinions and informal language

Note: This is a read-only operation that returns the raw response text.
""",
        schema=OpenGradientReadWorkflow,
    )
    def prompt_dobby(self, args: dict[str, Any]) -> str:
        """Prompts the Dobby-unhinged-8B model on the OpenGradient network.

        Args:
            args (dict[str, Any]): Input arguments for the action.

        Returns:
            str: A message containing the action response or error details.

        """
        try:
            prompt = args["prompt"]
            temperature = args["temperature"]
            max_tokens = args["max_tokens"]
            
            message = [{
                "role": "user",
                "content": prompt,
            }]

            llm_output = og.llm_chat(model_cid=og.LLM.DOBBY_UNHINGED_3_1_8B,
                                     messages=message, 
                                     temperature=temperature,
                                     max_tokens=max_tokens)
            
            return llm_output.chat_output.get("content", "Error: 'content' was not found in the chat output for the dobby model")
        except Exception as e:
            return f"Error reading one_hour_eth_usdt_volatility workflow: {e!s}"

    @create_action(
        name="prompt_qwen",
        description="""
This tool generates responses using the Qwen2.5-72B-Instruct model, a language model with strong capabilities in coding, mathematics, and multilingual tasks.
Do not use this tool for other LLM models or prompt formats.

Inputs:
- prompt: String containing the input prompt for the model
- temperature: (Optional, default=0.95) Float between 0.0 and 2.0 controlling randomness (higher = more random)
- max_tokens: (Optional, default=2048) Integer specifying maximum length of generated response

Output:
- Returns a string containing the model's response text
Example output: "Here's a Python implementation of merge sort:
def merge_sort(arr):
   if len(arr) <= 1:
       return arr
   mid = len(arr) // 2
   left = merge_sort(arr[:mid])
   right = merge_sort(arr[mid:])
   return merge(left, right)"

Important notes:
- Model excels at:
 - Complex coding tasks and mathematical reasoning
 - Structured data understanding and JSON generation
 - Long-form content generation (up to 8K tokens)
 - Multilingual responses across 29+ languages
- Temperature controls response variability:
 - 0.0: Most deterministic (good for coding/math)
 - 0.7: Balanced creativity (default)
 - 2.0: Maximum randomness

Note: This is a read-only operation that returns the raw response text.
""",
        schema=OpenGradientReadWorkflow,
    )
    def prompt_qwen(self, args: dict[str, Any]) -> str:
        """Prompts the Qwen-2.5-72B model on the OpenGradient network.

        Args:
            args (dict[str, Any]): Input arguments for the action.

        Returns:
            str: A message containing the action response or error details.

        """
        try:
            prompt = args["prompt"]
            temperature = args["temperature"]
            max_tokens = args["max_tokens"]
            
            message = [{
                "role": "user",
                "content": prompt,
            }]

            llm_output = og.llm_chat(model_cid=og.LLM.QWEN_2_5_72B_INSTRUCT,
                                     messages=message, 
                                     temperature=temperature,
                                     max_tokens=max_tokens)
            
            return llm_output.chat_output.get("content", "Error: 'content' was not found in the chat output for the qwen model")
            return ""
        except Exception as e:
            return f"Error reading one_hour_eth_usdt_volatility workflow: {e!s}"  
        
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
