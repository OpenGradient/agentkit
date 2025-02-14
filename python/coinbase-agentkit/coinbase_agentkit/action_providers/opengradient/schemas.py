"""Schemas for OpenGradient action provider."""

from pydantic import BaseModel, Field
from typing import Callable


class OpenGradientReadWorkflow(BaseModel):
    """Input schema for OpenGradient Read Workflow action."""

    contract_address: str = Field(..., description="The smart contract address of the OpenGradient workflow to read from")
    
    ## TODO (Kyle, Adam): Figure out if we should really include this function -- it's quite hard to implement and might be very arbitrary for the LLM to fill-in
    # output_formatter: Callable[[ModelOutput], str] = Field(default=lambda x : x, description="A function to format the output of the workflow")

class OpenGradientRunModel(BaseModel):
    """Input schema for OpenGradient Run Model action."""

    model_cid: str = Field(..., description="The unique CID for the model you want to run") 
    # input: 
    # input_schema: 
    # inference_mode:  
    # vault_address: str = Field(..., description="The address of the Morpho Vault to withdraw from")
