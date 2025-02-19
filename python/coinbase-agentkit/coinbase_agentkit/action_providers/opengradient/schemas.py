"""Schemas for OpenGradient action provider."""

from pydantic import BaseModel, Field
from typing import Callable

"""
1 Hour ETH/USDT volatility forecast workflow deployed at: 0xFC5d8EDba288f9330Af324555F1A729303382725
https://hub.opengradient.ai/models/OpenGradient/og-1hr-volatility-ethusdt
6 Hour SUI/USD forecast workflow deployed at: 0x080881b65427Da162CA0995fB23710Db4E8d85Cb
https://hub.opengradient.ai/models/OpenGradient/og-6h-return-suiusdt
30min SUI/USD forecast workflow deployed at: 0x7259f3a882B40aF80F7ff51D6023f23DD16b4465
https://hub.opengradient.ai/models/OpenGradient/og-30min-return-suiusdt
"""


class OpenGradientReadWorkflow(BaseModel):
    """Input schema for generic OpenGradient Read Workflow action."""

    contract_address: str = Field(..., description="The smart contract address of the OpenGradient workflow to read from")
    
    ## TODO (Kyle, Adam): Figure out if we should really include this function -- it's quite hard to implement and might be very arbitrary for the LLM to fill-in
    # output_formatter: Callable[[ModelOutput], str] = Field(default=lambda x : x, description="A function to format the output of the workflow")

class OpenGradientEthUsdtOneHourVolatilityForecast(BaseModel):
    """
    Input schema for OpenGradient 1 hour ETH/USDT volatility forecast from workflow. 
    More information at https://hub.opengradient.ai/models/OpenGradient/og-1hr-volatility-ethusdt
    """

class OpenGradientSuiUsdtSixHourReturnForecast(BaseModel):
    """
    Input schema for OpenGradient 6 hour SUI/USDT return forecast from workflow. 
    More information at https://hub.opengradient.ai/models/OpenGradient/og-6h-return-suiusdt
    """

class OpenGradientSuiUsdt30MinReturnForecast(BaseModel):
    """
    Input schema for OpenGradient 30 minute SUI/SDT return forecast from workflow.
    More information at https://hub.opengradient.ai/models/OpenGradient/og-30min-return-suiusdt
    """

class OpenGradientPromptDobby(BaseModel):
    """
    Input schema for prompting the OpenGradient hosted Dobby-Unhinged LLM.
    """
    prompt: str = Field(..., description="The prompt that you are asking the Dobby model")
    temperature: float = Field(default=0.95, description="The temperature of the LLM inference -- default is 0.95")
    max_tokens: int = Field(default=2048, description="The maximum number of tokens that Dobby can return -- default is 500")

class OpenGradientPromptQwen(BaseModel):
    """
    Input schema for prompting the OpenGradient hosted Qwen-2.5-70B LLM.
    """
    prompt: str = Field(..., description="The prompt that you are asking the Qwen model")
    temperature: float = Field(default=0.95, description="The prompt that you are asking the Qwen model. Default value is 0.95")
    max_tokens: int = Field(default=2048, description="The maximum number of tokens that Qwen can return. Default value is 500")

class OpenGradientRunModel(BaseModel):
    """Input schema for generic OpenGradient Run Model action."""

    model_cid: str = Field(..., description="The unique CID for the model you want to run") 
    # input: 
    # input_schema: 
    # inference_mode:  
    # vault_address: str = Field(..., description="The address of the Morpho Vault to withdraw from")
