"""Schemas for OpenGradient action provider."""

from pydantic import BaseModel, Field


class OpenGradientEthUsdtOneHourVolatilityForecast(BaseModel):
    """Input schema for OpenGradient 1 hour ETH/USDT volatility forecast from workflow.

    More information at https://hub.opengradient.ai/models/OpenGradient/og-1hr-volatility-ethusdt
    """


class OpenGradientSuiUsdtSixHourReturnForecast(BaseModel):
    """Input schema for OpenGradient 6 hour SUI/USDT return forecast from workflow.

    More information at https://hub.opengradient.ai/models/OpenGradient/og-6h-return-suiusdt
    """


class OpenGradientSuiUsdt30MinReturnForecast(BaseModel):
    """Input schema for OpenGradient 30 minute SUI/SDT return forecast from workflow.

    More information at https://hub.opengradient.ai/models/OpenGradient/og-30min-return-suiusdt
    """


class OpenGradientPromptDobby(BaseModel):
    """Input schema for prompting the OpenGradient hosted Dobby-Unhinged LLM."""

    prompt: str = Field(..., description="The prompt that you are asking the Dobby model")
    temperature: float = Field(
        default=0.95, description="The temperature of the LLM inference -- default is 0.95"
    )
    max_tokens: int = Field(
        default=2048,
        description="The maximum number of tokens that Dobby can return -- default is 2048",
    )


class OpenGradientPromptQwen(BaseModel):
    """Input schema for prompting the OpenGradient hosted Qwen-2.5-70B LLM."""

    prompt: str = Field(..., description="The prompt that you are asking the Qwen model")
    temperature: float = Field(
        default=0.95,
        description="The prompt that you are asking the Qwen model. Default value is 0.95",
    )
    max_tokens: int = Field(
        default=2048,
        description="The maximum number of tokens that Qwen can return. Default value is 2048",
    )
